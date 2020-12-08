from django.db.migrations.serializer import DecimalSerializer
from rest_framework import serializers

from customer.models import Customer, Order


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class AndroidOrderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='customer.name')
    lat = serializers.FloatField(source='customer.latitude')
    lon = serializers.FloatField(source='customer.longitude')
    address = serializers.CharField(source='customer.address')
    route_number = serializers.IntegerField(source='route.route_number')
    route_index = serializers.IntegerField(source='route.route_index')

    class Meta:
        model = Order
        fields = '__all__'
