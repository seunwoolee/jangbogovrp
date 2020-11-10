from django.urls import path, include

from company.views import get_company, kakao_sign_up

urlpatterns = [
    path('get_company/', get_company, name='get_company'),
    path('kakao_sign_up/', kakao_sign_up, name='kakao_sign_up'),
]
