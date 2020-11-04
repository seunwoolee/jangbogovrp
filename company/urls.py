from django.urls import path, include

from company.views import get_company

urlpatterns = [
    path('get_company/', get_company, name='get_company'),
]
