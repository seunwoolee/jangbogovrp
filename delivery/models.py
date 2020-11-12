from django.db import models

from core.models import TimeStampedModel
from company.models import Company, Driver


class RouteM(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='+')
    date = models.DateField()
    is_am = models.BooleanField()
    count_car = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    count_location = models.PositiveIntegerField()


class RouteD(TimeStampedModel):
    route_m = models.ForeignKey(RouteM, on_delete=models.CASCADE, related_name='details')
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='+')
    route_number = models.PositiveIntegerField()
    route_index = models.PositiveIntegerField()
    distance = models.PositiveIntegerField(default=0)
    json_map = models.TextField(null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, related_name='+', null=True, blank=True, default=None)

    class Meta:
        ordering = ['route_number', 'route_index', 'id']