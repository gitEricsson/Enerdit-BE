from django.db import models
from authentication.models import User

class Building(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    building_type = models.CharField(max_length=255)
    num_floors = models.IntegerField()
    total_energy_consumed = models.FloatField(default=0.0)  # Total kWh
    total_energy_cost = models.FloatField(default=0.0)  # In Naira
    energy_consumption_score = models.FloatField(default=0.0)  # Energy consumption score

    def __str__(self):
        return f"{self.building_type} - {self.num_floors} Floors"

class Compartment(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='compartments')
    name = models.CharField(max_length=255)
    total_energy_consumed = models.FloatField(default=0.0)  # in kWh
    total_energy_cost = models.FloatField(default=0.0)  # in currency

    def __str__(self):
        return f"{self.name} - {self.building}"

class Appliance(models.Model):
    compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE, related_name='appliances')
    name = models.CharField(max_length=255)
    power_rating = models.FloatField()  # in kW
    usage_time = models.FloatField()  # in hours
    total_energy_consumed = models.FloatField(default=0.0)  # in kWh
    total_energy_cost = models.FloatField(default=0.0)  # in currency

    def __str__(self):
        return f"{self.name} - {self.compartment}"

class EnergyConsumptionScore(models.Model):
    building = models.OneToOneField(Building, on_delete=models.CASCADE)
    score = models.FloatField()  # comparison against standard average consumption
