from datetime import date
from typing import List, Tuple, Dict

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company
from customer.models import Order, Customer, MutualDistance
from delivery.models import RouteM
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


@api_view(['PATCH'])
def update_course_number(request: Request) -> Response:
    guest_id = request.data.get('guest_id', '')
    to_course_number = request.data.get('to_course_number', '')
    erp_db = ERPDB()
    erp_db.update_customer_course_number(guest_id, to_course_number)
    return Response(status=200)


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
    is_am = request.data.get('isAm', True)
    user: User = request.user
    company: Company = user.company_info.first()
    erp_db = ERPDB()
    orders: list = erp_db.get_order_data(company.code, is_am=is_am)

    RouteM.objects.filter(Q(company=company), Q(is_am=is_am), Q(date=date.today())).delete()

    for order in orders:
        if not order['lat'] or not order['lon']:
            return Response(data={"message": "수집되지 않은 좌표가 있습니다."}, status=400)

        if order['courseNumber'] == 0 or order['courseNumber'] is None:
            return Response(data={"message": "코스번호가 없는 거래처가 있습니다."}, status=400)

    for order in orders:

        if order['pay'] < 0:
            order['pay'] = abs(order['pay'])

        customer = Customer.objects.filter(customer_id=order['guestId']).first()
        if customer:
            customer.address = order['address']
            customer.latitude = order['lat']
            customer.longitude = order['lon']
            customer.course_number = order['courseNumber']
            customer.save()
        else:
            customer = Customer.objects.create(
                customer_id=order['guestId'],
                name=order['name'],
                address=order['address'],
                latitude=order['lat'],
                longitude=order['lon'],
                course_number=order['courseNumber']
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

    return Response(status=200)


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
