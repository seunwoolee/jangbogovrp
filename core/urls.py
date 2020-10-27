from django.urls import path, include

from core.views import create_route, create_route_manual

urlpatterns = [
    path('create_route/', create_route, name='create_route'),
    path('create_route_manual/', create_route_manual, name='create_route_manual'),
]
