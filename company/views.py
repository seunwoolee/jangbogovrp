from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company
from company.serializers import CompanySerializer


@api_view(['GET'])
def get_company(request: Request) -> Response:
    user: User = request.user
    company: Company = Company.objects.get(manager=user)
    serializer = CompanySerializer(company)
    return Response(data=serializer.data, status=200)
