from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from mssql_service import ERPDB


@api_view(['GET'])
def preview_order(request: Request) -> Response:
    is_am = request.query_params.get('isAm', '')
    is_am = True if is_am == 'true' else False
    erp_db = ERPDB()
    result: list = erp_db.get_order_data(is_am=is_am)
    return Response(data=result, status=200)


@api_view(['GET'])
def pre_processing_geolocations(request: Request) -> Response:
    is_am = request.query_params.get('isAm', '')
    is_am = True if is_am == 'true' else False
    erp_db = ERPDB()
    orders: list = erp_db.pre_processing_geolocations(is_am=is_am)
    return Response(data=orders, status=200)


@api_view(['GET'])
def save_geolocation(request: Request) -> Response:
    order_number = request.query_params.get('orderNumber', '')
    lat = request.query_params.get('lat', '')
    lon = request.query_params.get('lon', '')
    erp_db = ERPDB()
    erp_db.update_geolocation(order_number, lat, lon)
    return Response(data=[], status=200)
