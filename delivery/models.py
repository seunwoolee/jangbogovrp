from django.db import models

from core.models import TimeStampedModel
from company.models import Company


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
    json_map = models.TextField(null=True, blank=True)
