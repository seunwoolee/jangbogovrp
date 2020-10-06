from django.contrib.auth.models import User
from django.db import models

from company.models import Company
from core.models import TimeStampedModel
from delivery.models import RouteD


class Customer(TimeStampedModel):
    customer_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=20, decimal_places=10)
    longitude = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    order_id = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='+')
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    route = models.ForeignKey(RouteD, on_delete=models.CASCADE, related_name='route_orders', null=True, blank=True)
    price = models.PositiveIntegerField()
    is_am = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.customer.name}({self.price}원) {self.date} ({self.is_am})'


class MutualDistance(TimeStampedModel):
    start = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='+')
    end = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='+')
    distance = models.PositiveIntegerField()
    json_map = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'from {self.start} -> {self.end} distance {self.distance}'
