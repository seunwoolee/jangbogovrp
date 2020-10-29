from typing import Dict, Union, List
from django.contrib.auth.models import User
from django.db.models import Max, Q, QuerySet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company
from core.vrp import VRP
from customer.models import Order
from delivery.models import RouteM, RouteD


@api_view(['POST'])
def create_route(request: Request) -> Response:
    delivery_date = request.data.get('deliveryDate', '')
    car_count = request.data.get('carCount', '')
    is_am = request.data.get('isAm', True)

    user: User = request.user
    code: str = user.company_info.first().code
    vrp: VRP = VRP(code, delivery_date, is_am, int(car_count))
    data: Dict[str, Union[list, int]] = vrp.create_data_model()
    routes: List[List] = vrp.vrp(data)
    route_m_id: int = vrp.save_route(routes)
    max_route_number = RouteD.objects.filter(route_m__id=route_m_id).aggregate(max_route_number=Max('route_number'))
    result = {'route_m_id': route_m_id, **max_route_number}

    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_route_manual(request: Request) -> Response:
    delivery_date = request.data.get('deliveryDate', '')
    is_am = request.data.get('isAm', True)

    user: User = request.user
    code: str = user.company_info.first().code
    vrp: VRP = VRP(code, delivery_date, is_am, 0)  # TODO 하드코딩
    route_m_id: int = vrp.save_route_manual()
    max_route_number = RouteD.objects.filter(route_m__id=route_m_id).aggregate(max_route_number=Max('route_number'))
    result = {'route_m_id': route_m_id, **max_route_number}

    return Response(data=result, status=status.HTTP_200_OK)
