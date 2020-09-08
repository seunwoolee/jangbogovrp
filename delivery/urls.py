from django.urls import path, include

from delivery.views import deliveries, map_groups

urlpatterns = [
    path('deliveries/', deliveries, name='deliveries'),
    path('map_groups/', map_groups, name='map_groups'),
]
