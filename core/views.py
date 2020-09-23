from datetime import datetime
from typing import Dict, Union, List

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from datetime import date

from core.vrp import VRP
from delivery.models import RouteD, RouteM
from delivery.serializers import RouteDSerializer


@api_view(['GET'])
def create_route(request: Request) -> Response:
    RouteM.objects.all().delete()
    user: User = request.user
    code: str = user.company_info.first().code
    vrp: VRP = VRP(code, '2020-09-21')
    data: Dict[str, Union[list, int]] = vrp.create_data_model()
    routes: List[List] = vrp.vrp(data)
    vrp.save_route(routes)

    routes = RouteD.objects.all()
    serializer = RouteDSerializer(routes, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
