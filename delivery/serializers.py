from rest_framework import serializers

from customer.serializers import CustomerSerializer
from delivery.models import RouteD


class RouteDSerializer(serializers.ModelSerializer):
    customer_info = CustomerSerializer(source='customer', read_only=True)

    class Meta:
        model = RouteD
        fields = '__all__'
