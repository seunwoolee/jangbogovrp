from django.db import models

from core.models import TimeStampedModel
from company.models import Company
from customer.models import Order


class RouteM(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='+')
    date = models.DateTimeField()
    is_am = models.BooleanField()
    count_car = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    count_location = models.PositiveIntegerField()


class RouteD(TimeStampedModel):
    route_m = models.ForeignKey(RouteM, on_delete=models.CASCADE, related_name='details')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='route')
    car_number = models.PositiveIntegerField()
    car_index = models.PositiveIntegerField()
    json_map = models.TextField()
