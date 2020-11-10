from django.contrib.auth.models import User
from rest_framework import serializers

from company.models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='auth_token', read_only=True)

    class Meta:
        model = User
        fields = '__all__'
