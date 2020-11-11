from django.urls import path, include

from delivery.views import deliveries, map_groups, maps, routeD, routeDUpdate, routeDManualUpdate, add_routeD, \
    delete_routeD, add_driver_to_routeD

urlpatterns = [
    path('deliveries/', deliveries, name='deliveries'),
    path('map_groups/', map_groups, name='map_groups'),
    path('maps/', maps, name='maps'),
    path('routeD/', routeD, name='routeD'),
    path('routeDUpdate/', routeDUpdate, name='routeDUpdate'),
    path('routeDManualUpdate/', routeDManualUpdate, name='routeDManualUpdate'),
    path('add_routeD/', add_routeD, name='add_routeD'),
    path('delete_routeD/', delete_routeD, name='delete_routeD'),
    path('add_driver_to_routeD/', add_driver_to_routeD, name='add_driver_to_routeD'),
]
