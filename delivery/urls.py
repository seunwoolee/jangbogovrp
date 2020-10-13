from django.urls import path, include

from delivery.views import deliveries, map_groups, maps, routeD, routeDUpdate, routeDManualUpdate

urlpatterns = [
    path('deliveries/', deliveries, name='deliveries'),
    path('map_groups/', map_groups, name='map_groups'),
    path('maps/', maps, name='maps'),
    path('routeD/', routeD, name='routeD'),
    path('routeDUpdate/', routeDUpdate, name='routeDUpdate'),
    path('routeDManualUpdate/', routeDManualUpdate, name='routeDManualUpdate'),
]
