from rest_framework import serializers
from .models import Building, Compartment, Appliance

class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ['name', 'power_rating', 'usage_time', 'total_energy_consumed', 'total_energy_cost']

class CompartmentSerializer(serializers.ModelSerializer):
    appliances = ApplianceSerializer(many=True)

    class Meta:
        model = Compartment
        fields = ['name', 'total_energy_consumed', 'total_energy_cost', 'appliances']

class BuildingSerializer(serializers.ModelSerializer):
    compartments = CompartmentSerializer(many=True)

    class Meta:
        model = Building
        fields = ['user', 'building_type', 'num_floors', 'compartments']

    def create(self, validated_data):
        compartments_data = validated_data.pop('compartments')
        building = Building.objects.create(**validated_data)
        
        # For each compartment
        for compartment_data in compartments_data:
            appliances_data = compartment_data.pop('appliances')
            compartment = Compartment.objects.create(building=building, **compartment_data)
            
            # For each appliance in the compartment
            for appliance_data in appliances_data:
                Appliance.objects.create(compartment=compartment, **appliance_data)
        
        return building
