from django.contrib.auth.models import User
from django.db import models

from core.models import TimeStampedModel


class Company(TimeStampedModel):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_info')
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    erp_url = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Driver(TimeStampedModel):
    name = models.CharField(max_length=30)
    course_number = models.PositiveSmallIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver', null=True, blank=True)
