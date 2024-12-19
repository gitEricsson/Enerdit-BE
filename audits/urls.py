from django.urls import path
from .views import BuildingEnergyAuditView

urlpatterns = [
    path('energy-audit/', BuildingEnergyAuditView.as_view(), name='energy-audit'),
]
