from django.shortcuts import render
from datetime import datetime
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from mysql_service import DB


@api_view(['GET'])
def deliveries(request: Request) -> Response:
    start_date = request.query_params.get('startDate', '')
    end_date = request.query_params.get('endDate', '')
    is_am = request.query_params.get('isAm', True)
    mysql = DB()

    result: list = mysql.get_delivery_list(start_date, end_date)
    return Response(data=result, status=200)


@api_view(['GET'])
def map_groups(request: Request) -> Response:
    vs_seq = request.query_params.get('vs_seq', '')
    mysql = DB()
    vehicle_allocate_status: dict = mysql.get_vehicle_allocate_status(vs_seq)
    delivery_date: datetime = vehicle_allocate_status['vs_deliveryDate']
    delivery_date: str = delivery_date.strftime('%Y-%m-%d')
    result: list = mysql.get_map_group_list(delivery_date, vehicle_allocate_status['vs_meridiemType'])
    return Response(data=result, status=200)
