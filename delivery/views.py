from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company
from delivery.models import RouteM
from delivery.serializers import RouteMSerializer, RouteMDSerializer
from mysql_service import DB


@api_view(['GET'])
def deliveries(request: Request) -> Response:
    start_date = request.query_params.get('startDate', '')
    end_date = request.query_params.get('endDate', '')
    user: User = request.user
    company: Company = user.company_info.first()
    route_m = RouteM.objects.filter(Q(company=company), Q(date__gte=start_date), Q(date__lte=end_date))
    serializer = RouteMSerializer(route_m, many=True)

    return Response(data=serializer.data, status=200)


@api_view(['GET'])
def map_groups(request: Request) -> Response:
    route_m_id = request.query_params.get('routeMId', '')
    mysql = DB()
    vehicle_allocate_status: dict = mysql.get_vehicle_allocate_status(route_m_id)
    delivery_date: datetime = vehicle_allocate_status['vs_deliveryDate']
    delivery_date: str = delivery_date.strftime('%Y-%m-%d')
    result: list = mysql.get_map_group_list(delivery_date, vehicle_allocate_status['vs_meridiemType'])
    return Response(data=result, status=200)


@api_view(['GET'])
def maps(request: Request) -> Response:
    route_m: str = request.query_params.get('routeM', '')
    route_m = RouteM.objects.get(id=route_m)
    serializer = RouteMDSerializer(route_m)
    return Response(data=serializer.data, status=200)
