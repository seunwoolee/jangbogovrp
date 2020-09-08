from django.urls import path, include

from customer.views import preview_order

urlpatterns = [
    path('preview_order/', preview_order, name='preview_order'),
]
