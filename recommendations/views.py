from .models import EnergySavingRecommendation

def add_recommendations():
    recommendations = [
        # HVAC Optimization
        {"category": "HVAC", "recommendation": "Install a programmable thermostat to reduce energy use during off-hours."},
        {"category": "HVAC", "recommendation": "Regularly clean and replace air filters to maintain system efficiency."},
        {"category": "HVAC", "recommendation": "Insulate air ducts to prevent energy losses during heating or cooling."},
        {"category": "HVAC", "recommendation": "Seal windows and doors to reduce air leakage and lower HVAC strain."},
        {"category": "HVAC", "recommendation": "Upgrade to a high-efficiency HVAC system (Energy Star-rated)."},
        {"category": "HVAC", "recommendation": "Utilize zoning systems to avoid heating or cooling unoccupied areas."},
        {"category": "HVAC", "recommendation": "Maintain HVAC units through regular professional servicing."},
        {"category": "HVAC", "recommendation": "Install ceiling fans to reduce HVAC load by improving air circulation."},
        {"category": "HVAC", "recommendation": "Use energy recovery ventilators to reduce the load on heating and cooling."},
        {"category": "HVAC", "recommendation": "Implement demand-controlled ventilation to adjust fresh air supply based on occupancy."},
        
        # Lighting Efficiency
        {"category": "Lighting", "recommendation": "Replace incandescent bulbs with energy-efficient LEDs."},
        {"category": "Lighting", "recommendation": "Install motion sensors to ensure lights are off in unoccupied areas."},
        {"category": "Lighting", "recommendation": "Use daylight sensors to automatically adjust lighting based on natural light availability."},
        {"category": "Lighting", "recommendation": "Implement dimmer switches to lower energy consumption during low-light needs."},
        {"category": "Lighting", "recommendation": "Use task lighting instead of overhead lighting in work areas."},
        {"category": "Lighting", "recommendation": "Optimize window coverings to maximize daylight usage and minimize artificial lighting."},
        {"category": "Lighting", "recommendation": "Group light controls for better management of zones."},
        {"category": "Lighting", "recommendation": "Replace exit signs with LED models for continuous energy savings."},
        {"category": "Lighting", "recommendation": "Choose lighting fixtures with reflective finishes to improve light distribution."},
        {"category": "Lighting", "recommendation": "Use timers or smart controls to ensure outdoor lighting is used efficiently."},
        
        # Appliance Management
        {"category": "Appliance", "recommendation": "Unplug appliances when not in use to avoid phantom power drain."},
        {"category": "Appliance", "recommendation": "Choose Energy Star-rated appliances to reduce electricity usage."},
        {"category": "Appliance", "recommendation": "Use smart plugs to control when appliances are on or off remotely."},
        {"category": "Appliance", "recommendation": "Set refrigerators and freezers to the optimal temperature for energy savings."},
        {"category": "Appliance", "recommendation": "Regularly clean appliance coils to ensure efficient operation."},
        {"category": "Appliance", "recommendation": "Turn off computers and electronics when not in use or set them to sleep mode."},
        {"category": "Appliance", "recommendation": "Upgrade older appliances to energy-efficient models."},
        {"category": "Appliance", "recommendation": "Use cold water settings on washing machines to save on heating costs."},
        {"category": "Appliance", "recommendation": "Ensure that dishwashers are fully loaded before running."},
        {"category": "Appliance", "recommendation": "Air-dry clothes instead of using electric dryers whenever possible."},
        
        # Natural Cooling
        {"category": "Natural", "recommendation": "Install reflective roofing materials to reduce heat absorption."},
        {"category": "Natural", "recommendation": "Use window shades, blinds, or curtains to block direct sunlight during hot periods."},
        {"category": "Natural", "recommendation": "Plant shade trees near windows to reduce solar heat gain."},
        {"category": "Natural", "recommendation": "Install ventilation or exhaust fans in areas prone to heat buildup."},
        {"category": "Natural", "recommendation": "Use cross-ventilation to naturally cool the home by opening windows on opposite sides."},
        {"category": "Natural", "recommendation": "Optimize building insulation to maintain cooler indoor temperatures."},
        {"category": "Natural", "recommendation": "Install window films to reduce heat gain without losing natural light."},
        {"category": "Natural", "recommendation": "Create shaded outdoor areas using pergolas or awnings to reduce indoor cooling needs."},
        {"category": "Natural", "recommendation": "Use cool or green roofs to reflect sunlight and reduce roof temperature."},
        {"category": "Natural", "recommendation": "Design landscaping to promote natural breezes around the building."}
    ]
    
    # Insert recommendations into the database
    for rec in recommendations:
        EnergySavingRecommendation.objects.create(**rec)
