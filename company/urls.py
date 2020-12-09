from django.urls import path, include

from company.views import get_company, kakao_sign_up, create_driver, delete_driver, get_drivers, create_push_key

urlpatterns = [
    path('get_company/', get_company, name='get_company'),
    path('kakao_sign_up/', kakao_sign_up, name='kakao_sign_up'),
    path('create_driver/', create_driver, name='create_driver'),
    path('delete_driver/', delete_driver, name='delete_driver'),
    path('get_drivers/', get_drivers, name='get_drivers'),
    path('create_push_key/', create_push_key, name='create_push_key'),
]
