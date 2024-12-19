from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import Building, Compartment, Appliance
from recommendations.models import EnergySavingRecommendation
from .utils import AppError
from .serializers import BuildingSerializer
import random
import os
import json
import google.generativeai as genai


from dotenv import load_dotenv
load_dotenv()

# Average estimated energy consumption for 1-9 floors(KWh/day)
STANDARD_AVERAGE_CONSUMPTION = {
    1: 61.5,  
    2: 123,  
    3: 184.5,  
    4: 246,  
    5: 307.5,  
    6: 369,  
    7: 430.5,  
    8: 492,  
    9: 553.5   
}

def calculate_energy_consumption_score(user_consumption, num_floors):
    if num_floors not in STANDARD_AVERAGE_CONSUMPTION:
        return (0.0, 0.0)  # Only considering 1-9 floors
    
    standard_avg = STANDARD_AVERAGE_CONSUMPTION.get(num_floors)
    
    if user_consumption <= standard_avg:
        return (100.0, standard_avg)  # Return as a tuple
    
    excess_ratio = (user_consumption - standard_avg) / standard_avg
    penalty_rate = 100
    
    score = 100 - (excess_ratio * penalty_rate)
    
    return max(round(score, 2), 0.0), standard_avg

class BuildingEnergyAuditView(APIView):
    permission_classes=[IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        building_type = request.data.get('building_type', '').lower()
        if building_type != 'residential':

            return Response(
                {"error": "This service currently only supports residential buildings."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            building = serializer.save()

            total_energy_building = 0.0
            total_cost_building = 0.0
            
            compartments_response = []

            for compartment in building.compartments.all():
                total_energy_compartment = 0.0
                total_cost_compartment = 0.0
                
                appliances_response = []

                for appliance in compartment.appliances.all():
                    # Energy consumed (kWh) = Power Rating (kW) * Usage Time (hours)
                    energy_consumed = appliance.power_rating * appliance.usage_time
                    appliance.total_energy_consumed = energy_consumed

                    # Cost per kWh (assuming ₦209.5 per kWh for band A feeders in Lagos state)
                    energy_cost = energy_consumed * 209.5  # Example cost per kWh
                    appliance.total_energy_cost = energy_cost

                    appliance.save()

                    total_energy_compartment += energy_consumed
                    total_cost_compartment += energy_cost
                    
                    appliances_response.append({
                        "name": appliance.name,
                        "power_rating": appliance.power_rating,
                        "usage_time": appliance.usage_time,
                        "total_energy_consumed": appliance.total_energy_consumed,
                        "total_energy_cost": appliance.total_energy_cost,
                    })

                # Save compartment totals
                compartment.total_energy_consumed = total_energy_compartment
                compartment.total_energy_cost = total_cost_compartment
                compartment.save()
                
                compartments_response.append({
                    "name": compartment.name,
                    "total_energy_consumed": total_energy_compartment,
                    "total_energy_cost": total_cost_compartment,
                    "appliances": appliances_response
                })

                total_energy_building += total_energy_compartment
                total_cost_building += total_cost_compartment

            building.total_energy_consumed = total_energy_building
            building.total_energy_cost = total_cost_building

            energy_score_percentage, standard_avg = calculate_energy_consumption_score(
                total_energy_building, building.num_floors
            )
            building.energy_consumption_score = energy_score_percentage
            building.save()
            
            recommendations = get_ai_recommendations({
            "building_type": building.building_type,
            "num_floors": building.num_floors,
            "compartments": compartments_response,            
            "total_energy_consumed": total_energy_building,
            "total_energy_cost": total_cost_building})
                        
            # recommendations = get_random_recommendations()
            
            response_data = {
            "building_type": building.building_type,
            "num_floors": building.num_floors,
            "compartments": compartments_response,            
            "total_energy_consumed": total_energy_building,
            "total_energy_cost": total_cost_building,
            "energy_consumption_score": f"{energy_score_percentage}%",
            "standard_average_consumption": standard_avg,
            "recommendations": recommendations}


            # Return the response with all the calculated results
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def get_random_recommendations():
    categories = ['HVAC', 'Lighting', 'Appliance', 'Natural']
    recommendations_by_category = []

    for category in categories:
        category_recommendations = EnergySavingRecommendation.objects.filter(category=category)
        
        count = category_recommendations.aggregate(count=Count('id'))['count']
        if count >= 2:
            random_recs = random.sample(list(category_recommendations), 2)
        else:
            random_recs = list(category_recommendations)

        recommendations_text = [rec.recommendation for rec in random_recs]
        
        recommendations_by_category.append({
            "category": category,
            "recommendations": recommendations_text
        })

    return recommendations_by_category

def get_ai_recommendations(data):
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""Please provide real-time intelligent and statistically personalised energy recommendations based on the following data: {data}
        Please provide the recommendations in the following JSON format:
        {{
            "recommendations": [
                {{
                    "category": "HVAC",
                    "recommendations": [
                        "recommendation 1",
                        "recommendation 2"
                    ]
                }},
                {{
                    "category": "Lighting",
                    "recommendations": [
                        "recommendation 1",
                        "recommendation 2"
                    ]
                }},
                {{
                    "category": "Appliance",
                    "recommendations": [
                        "recommendation 1",
                        "recommendation 2"
                    ]
                }},
                {{
                    "category": "Natural",
                    "recommendations": [
                        "recommendation 1",
                        "recommendation 2"
                    ]
                }}
            ]
        }}"""
        response = model.generate_content(prompt)
        text_content = response.text    
        json_str = text_content.replace('```json', '').replace('```', '').strip()
        recommendations_dict = json.loads(json_str)
        
        return recommendations_dict["recommendations"]        
    except Exception as e:
                raise AppError(f'There was an error preparing the AI recommendations: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)