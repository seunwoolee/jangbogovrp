from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    """
        created , modified field 제공해주는 abstract base class model
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Info(TimeStampedModel):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_info')
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    erp_url = models.CharField(max_length=255)
    code = models.CharField(max_length=10) # TODO 뭐하는지 모름(대체 가능할듯)

    def __str__(self):
        return self.name