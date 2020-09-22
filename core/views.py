from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .tsp import tsp, create_data_model
from datetime import date


@api_view(['GET'])
def create_route(request: Request) -> Response:
    user: User = request.user
    code: str = user.company_info.first().code
    data: dict = create_data_model(code, '2020-09-21')
    tsp(data)
    return Response(data=data, status=200)
