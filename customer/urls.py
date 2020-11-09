from django.urls import path, include

from customer.views import preview_order, save_geolocation, create_customers, \
    save_mutual_distance, update_course_number, get_orders, get_customer

urlpatterns = [
    path('preview_order/', preview_order, name='preview_order'),
    path('update_course_number/', update_course_number, name='update_course_number'),
    path('save_geolocation/', save_geolocation, name='save_geolocation'),
    path('create_customers/', create_customers, name='create_customers'),
    path('save_mutual_distance/', save_mutual_distance, name='save_mutual_distance'),
    path('get_orders/', get_orders, name='get_orders'),
    path('get_customer/', get_customer, name='get_customer'),
]
