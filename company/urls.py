from django.urls import path, include

from company.views import get_company, kakao_sign_up, create_driver, delete_driver

urlpatterns = [
    path('get_company/', get_company, name='get_company'),
    path('kakao_sign_up/', kakao_sign_up, name='kakao_sign_up'),
    path('create_driver/', create_driver, name='create_driver'),
    path('delete_driver/', delete_driver, name='delete_driver'),
]
