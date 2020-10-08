from django.urls import path, include

from customer.views import preview_order, save_geolocation, create_customers, \
    save_mutual_distance

urlpatterns = [
    path('preview_order/', preview_order, name='preview_order'),
    path('save_geolocation/', save_geolocation, name='save_geolocation'),
    path('create_customers/', create_customers, name='create_customers'),
    path('save_mutual_distance/', save_mutual_distance, name='save_mutual_distance'),
]
