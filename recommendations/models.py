from django.db import models

# Create your models here.
class EnergySavingRecommendation(models.Model):
    CATEGORY_CHOICES = [
        ('HVAC', 'HVAC Optimization'),
        ('Lighting', 'Lighting Efficiency'),
        ('Appliance', 'Appliance Management'),
        ('Natural', 'Natural Cooling'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    recommendation = models.TextField()