from rest_framework import serializers

from customer.serializers import CustomerSerializer, OrderSerializer
from delivery.models import RouteD, RouteM


class RouteDSerializer(serializers.ModelSerializer):
    customer_info = CustomerSerializer(source='customer', read_only=True)
    orders = OrderSerializer(source='route_orders', read_only=True, many=True)

    class Meta:
        model = RouteD
        fields = '__all__'


class RouteMDSerializer(serializers.ModelSerializer):
    route_d = RouteDSerializer(source='details', read_only=True, many=True)

    class Meta:
        model = RouteM
        fields = '__all__'


class RouteMSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteM
        fields = '__all__'
