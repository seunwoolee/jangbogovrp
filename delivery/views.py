import requests
from django.contrib.auth.models import User
from django.db.models import Q, Max, QuerySet
from django.shortcuts import render
from datetime import datetime, date
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company, Driver
from customer.models import Customer
from delivery.models import RouteM, RouteD
from delivery.serializers import RouteMSerializer, RouteMDSerializer, RouteDSerializer, RouteDOrderSerializer
from mssql_service import ERPDB
from mysql_service import DB


@api_view(['GET'])
def deliveries(request: Request) -> Response:
    start_date = request.query_params.get('startDate', '')
    end_date = request.query_params.get('endDate', '')
    user: User = request.user
    company: Company = user.company_info.first()
    route_m: QuerySet[RouteM] = RouteM.objects.filter(
        Q(company=company), Q(date__gte=start_date), Q(date__lte=end_date))
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


@api_view(['PATCH'])
def routeDUpdate(request: Request) -> Response:
    routes: list = request.data

    for route in routes:
        route_m_id = route.get('routeM', '')
        customer_id = route.get('customerId', '')
        route_index = route.get('index', '')
        json_data = route.get('jsonData', '')
        total_distance = route.get('totalDistance', '')

        route_d = RouteD.objects.get(Q(customer__id=customer_id), Q(route_m__id=route_m_id))
        route_d.route_index = route_index
        route_d.json_map = None

        if json_data:
            route_d.json_map = json_data
            user = request.user
            company: Company = user.company_info.first()

            # TODO 하드코딩
            if company.code == '011':
                driver = Driver.objects.filter(Q(course_number=route_d.route_number), Q(company=company)).first()
            else:
                driver = Driver.objects.filter(course_number=route_d.route_number).first()

            route_d.driver = driver

        if total_distance:
            route_d.distance = total_distance
        else:
            route_d.distance = 0

        route_d.save()
    return Response(status=200)


@api_view(['POST'])
def routeDManualUpdate(request: Request) -> Response:
    route_m_id = request.data.get('route_m_id', '')
    to_route_number = request.data.get('to_route_number', '')
    from_route_number = request.data.get('from_route_number', '')
    current_route_index = request.data.get('current_route_index', '')
    is_duplicated = request.data.get('is_duplicated', False)
    duplicated_count = 1

    from_route_d: RouteD = RouteD.objects.get(
        Q(route_m__id=route_m_id), Q(route_number=from_route_number), Q(route_index=current_route_index))

    to_max_route_index: dict = RouteD.objects.filter(
        Q(route_m__id=route_m_id), Q(route_number=to_route_number)).aggregate(max_route_index=Max('route_index'))

    from_route_d.route_number = to_route_number

    if to_max_route_index.get('max_route_index', None):
        from_route_d.route_index = to_max_route_index['max_route_index'] + 1
    else:
        from_route_d.route_index = 1

    from_route_d.save()

    if is_duplicated:
        from_route_ds: QuerySet[RouteD] = RouteD.objects \
            .exclude(Q(id=from_route_d.id)) \
            .filter(Q(route_m__id=route_m_id), Q(customer__latitude=from_route_d.customer.latitude),
                    Q(customer__longitude=from_route_d.customer.longitude), ~Q(route_number=from_route_d.route_number))

        next_route_index = from_route_d.route_index

        for route_d in from_route_ds:
            next_route_index += 1
            route_d.route_number = from_route_d.route_number
            route_d.route_index = next_route_index
            route_d.save()

        duplicated_count = from_route_ds.count() + 1

    route_ds: QuerySet[RouteD] = RouteD.objects.filter(
        Q(route_m__id=route_m_id), Q(route_number=from_route_number), Q(route_index__gt=current_route_index))

    for route_d in route_ds:
        route_d.route_index -= duplicated_count
        route_d.save()

    return Response(status=200)


@api_view(['POST'])
def add_routeD(request: Request) -> Response:
    customer_code: str = request.data.get('customerCode', '')
    route_number: str = request.data.get('routeNumber', '')
    route_m_id: int = request.data.get('routeM', '')

    try:
        customer = Customer.objects.get(customer_id=customer_code)
    except Customer.DoesNotExist:
        erp_db = ERPDB()
        result = erp_db.get_customer(customer_code)
        url = "https://apis.openapi.sk.com/tmap/geo/fullAddrGeo?version=1&format=json&callback=result"
        params = {
            'fullAddr': result['Address1'],
            'coordType': "WGS84GEO",
            'appKey': "0de9ecde-b87c-404c-b7f8-be4ed7b85d4f",
        }
        response = requests.get(url, params)
        data = response.json()
        coordinate_info = data['coordinateInfo']
        coordinate = coordinate_info['coordinate'][0]
        if coordinate['lat'] and coordinate['lon']:
            lat = coordinate['lat']
            lon = coordinate['lon']
        else:
            lat = coordinate['newLat']
            lon = coordinate['newLon']

        customer = Customer.objects.create(
            customer_id=result['CtCode'],
            name=result['JoinUserName'],
            address=result['Address1'],
            course_number=result['CourseNum'],
            latitude=lat,
            longitude=lon
        )
        customer.save()

    route_m = RouteM.objects.get(id=route_m_id)
    max_route_index = RouteD.objects.filter(Q(route_m=route_m), Q(route_number=route_number)).aggregate(
        index=Max('route_index'))

    RouteD.objects.create(
        route_m=route_m,
        route_number=route_number,
        route_index=max_route_index['index'] + 1,
        customer=customer
    ).save()

    return Response(status=200)


@api_view(['DELETE'])
def delete_routeD(request: Request) -> Response:
    route_d_id: int = request.data.get('routeD', '')
    RouteD.objects.get(id=route_d_id).delete()
    return Response(status=200)


@api_view(['POST'])
def add_driver_to_routeD(request: Request) -> Response:
    driver_id: int = request.data.get('driver_id', '')
    route_d_id: int = request.data.get('route_d_id', '')
    route_d = RouteD.objects.get(id=route_d_id)
    driver = Driver.objects.get(id=driver_id)
    route_d.driver = driver
    route_d.save()
    return Response(status=200)


@api_view(['GET'])
def android_routeD(request: Request) -> Response:
    user: User = request.user
    driver: Driver = user.driver.first()
    today: str = date.today().strftime('%Y-%m-%d')

    route_d = RouteD.objects.filter(Q(driver=driver), Q(route_m__date=today)).first()

    if not route_d:
        return Response(data=[], status=200)

    route_ds = RouteD.objects.filter(
        Q(route_m__date=today), Q(route_number=route_d.route_number)).order_by('route_index')

    serializer = RouteDOrderSerializer(route_ds, many=True)
    return Response(data=serializer.data, status=200)