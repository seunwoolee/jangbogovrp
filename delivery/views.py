from django.contrib.auth.models import User
from django.db.models import Q, Max, QuerySet
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company
from delivery.models import RouteM, RouteD
from delivery.serializers import RouteMSerializer, RouteMDSerializer, RouteDSerializer, RouteDOrderSerializer
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


@api_view(['GET'])
def routeD(request: Request) -> Response:
    route_m: str = request.query_params.get('routeM', '')
    route_number: str = request.query_params.get('routeNumber', '')
    route_ds = RouteD.objects.filter(Q(route_m__id=route_m), Q(route_number=route_number)) \
        .exclude(customer__name="admin")
    serializer = RouteDOrderSerializer(route_ds, many=True)
    return Response(data=serializer.data, status=200)


@api_view(['patch'])
def routeDUpdate(request: Request) -> Response:
    route_m_id = request.data.get('routeM', '')
    customer_id = request.data.get('customerId', '')
    route_index = request.data.get('index', '')
    json_data = request.data.get('jsonData', '')

    route_d = RouteD.objects.get(Q(customer__id=customer_id), Q(route_m__id=route_m_id))
    route_d.route_index = route_index

    if json_data:
        route_d.json_map = json_data

    route_d.save()
    return Response(status=200)


@api_view(['POST'])
def routeDManualUpdate(request: Request) -> Response:
    route_m_id = request.data.get('route_m_id', '')
    to_route_number = request.data.get('to_route_number', '')
    from_route_number = request.data.get('from_route_number', '')
    current_route_index = request.data.get('current_route_index', '')

    from_route_d: RouteD = RouteD.objects.get(
        Q(route_m__id=route_m_id), Q(route_number=from_route_number), Q(route_index=current_route_index))

    to_max_route_index: dict = RouteD.objects.filter(
        Q(route_m__id=route_m_id), Q(route_number=to_route_number)).aggregate(max_route_index=Max('route_index'))

    from_route_d.route_number = to_route_number
    from_route_d.route_index = to_max_route_index['max_route_index'] + 1
    from_route_d.save()

    route_ds: QuerySet[RouteD] = RouteD.objects.filter(
        Q(route_m__id=route_m_id), Q(route_number=from_route_number), Q(route_index__gt=current_route_index))

    for route_d in route_ds:
        route_d.route_index -= 1
        route_d.save()

    return Response(status=200)
