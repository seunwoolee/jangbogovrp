from datetime import date
from typing import List, Tuple, Dict

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company
from customer.models import Order, Customer, MutualDistance
from mssql_service import ERPDB
from mysql_service import DB


@api_view(['GET'])
def preview_order(request: Request) -> Response:
    is_am = request.query_params.get('isAm', True)
    is_am = True if is_am == 'true' else False
    erp_db = ERPDB()
    user: User = request.user
    code: str = user.company_info.first().code
    result: list = erp_db.get_order_data(company_code=code, is_am=is_am)
    return Response(data=result, status=200)


@api_view(['GET'])
def pre_processing_geolocations(request: Request) -> Response:
    is_am = request.query_params.get('isAm', '')
    is_am = True if is_am == 'true' else False
    user: User = request.user
    company: Company = user.company_info.first()

    erp_db = ERPDB()
    orders: list = erp_db.pre_processing_geolocations(company.code, is_am=is_am)
    return Response(data=orders, status=200)


@api_view(['GET'])
def save_geolocation(request: Request) -> Response:
    order_number = request.query_params.get('orderNumber', '')
    lat = request.query_params.get('lat', '')
    lon = request.query_params.get('lon', '')
    erp_db = ERPDB()
    erp_db.update_geolocation(order_number, lat, lon)
    return Response(data=[], status=200)


@api_view(['POST'])
def create_customers(request: Request) -> Response:
    """
    고객 정보 업데이트 및 생성
    업데이트 및 생성된 고객은 Mutual_Distance create 필요
    :param request:
    :return: is_not_valid_customers
    """
    is_am = request.data.get('isAm', True)
    user: User = request.user
    company: Company = user.company_info.first()
    erp_db = ERPDB()
    orders: list = erp_db.get_order_data(company.code, is_am=is_am)
    if user.username == 'chilgok':
        starting_position: Customer = Customer.objects.filter(customer_id='chilgok').first()  # TODO 하드코딩
    else:
        starting_position: Customer = Customer.objects.filter(customer_id='admin').first()  # TODO 하드코딩

    all_customer_ids: list = [starting_position.id]

    Order.objects.filter(
        company=company,
        date=date.today(),
        is_am=is_am
    ).delete()

    for order in orders:
        if not order['lat'] or not order['lon']:
            return Response(data=order, status=400)

    for order in orders:
        customer = Customer.objects.filter(customer_id=order['guestId']).first()
        if customer:
            customer.address = order['address']
            customer.latitude = order['lat']
            customer.longitude = order['lon']
            customer.save()
        else:
            customer = Customer.objects.create(
                customer_id=order['guestId'],
                name=order['name'],
                address=order['address'],
                latitude=order['lat'],
                longitude=order['lon']
            )
            customer.save()

        Order.objects.create(
            order_id=order['orderNumber'],
            company=company,
            date=order['deliveryDate'],
            customer=customer,
            price=order['pay'],
            is_am=is_am,
        ).save()

        all_customer_ids.append(customer.id)

    invalid_mutual_distance_customers: List[Tuple] = []
    for start_customer_pk in all_customer_ids:
        for end_customer_pk in all_customer_ids:
            if start_customer_pk == end_customer_pk:
                continue

            if not MutualDistance.objects.filter(
                    Q(start__id=start_customer_pk), Q(end__id=end_customer_pk)):
                start = Customer.objects.get(id=start_customer_pk)
                end = Customer.objects.get(id=end_customer_pk)
                invalid_mutual_distance_customers.append(
                    (
                        {
                            'customer_id': start.id,
                            'lon': start.longitude,
                            'lat': start.latitude,
                        },
                        {
                            'customer_id': end.id,
                            'lon': end.longitude,
                            'lat': end.latitude,
                        },
                    )
                )

            if not MutualDistance.objects.filter(
                    Q(start__id=end_customer_pk), Q(end__id=start_customer_pk)):
                start = Customer.objects.get(id=end_customer_pk)
                end = Customer.objects.get(id=start_customer_pk)
                invalid_mutual_distance_customers.append(
                    (
                        {
                            'customer_id': start.id,
                            'lon': start.longitude,
                            'lat': start.latitude,
                        },
                        {
                            'customer_id': end.id,
                            'lon': end.longitude,
                            'lat': end.latitude,
                        },
                    )
                )

    # TODO MYSQL 에서 mutualDistance(start, end) 검색
    # 1. mysql가져오고 없으면 Tmap 던짐(test)
    mysql = DB()
    result: list = []
    for invalid_mutual_distance_customer in invalid_mutual_distance_customers:
        start = invalid_mutual_distance_customer[0]
        end = invalid_mutual_distance_customer[1]

        start_customer = Customer.objects.get(id=start['customer_id'])
        end_customer = Customer.objects.get(id=end['customer_id'])
        mutual_distance: dict = mysql.get_one_mutual_distance(start_customer.customer_id, end_customer.customer_id)
        if mutual_distance:
            MutualDistance.objects.create(
                start=start_customer,
                end=end_customer,
                distance=mutual_distance['vd_distanceValue'],
                json_map=mutual_distance['vd_jsonData']
            ).save()
        else:
            print(start_customer.customer_id, end_customer.customer_id)
            result.append(invalid_mutual_distance_customer)
    return Response(data=result, status=200) # TODO invalid_mutual_distance_customers을 던져야함


@api_view(['POST'])
def save_mutual_distance(request: Request) -> Response:
    temp = {}
    start = Customer.objects.get(id=request.data.get('start'))
    end = Customer.objects.get(id=request.data.get('end'))
    temp['start'] = start
    temp['end'] = end
    temp['distance'] = request.data.get('distance', '')
    temp['json_map'] = request.data.get('jsonMap', '')
    MutualDistance.objects.create(**temp).save()
    return Response(data=[], status=200)
