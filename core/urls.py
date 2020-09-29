from django.urls import path, include

from core.views import create_route

urlpatterns = [
    path('create_route/', create_route, name='create_route'),
]
