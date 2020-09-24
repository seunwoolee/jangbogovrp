from django.urls import path, include

from customer.views import preview_order, save_geolocation, pre_processing_geolocations

urlpatterns = [
    path('preview_order/', preview_order, name='preview_order'),
    path('pre_processing_geolocations/', pre_processing_geolocations, name='pre_processing_geolocations'),
    path('save_geolocation/', save_geolocation, name='save_geolocation'),
]
