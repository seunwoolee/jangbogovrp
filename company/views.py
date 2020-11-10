from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company
from company.serializers import CompanySerializer, UserSerializer


@api_view(['GET'])
def get_company(request: Request) -> Response:
    user: User = request.user
    company: Company = Company.objects.get(manager=user)
    serializer = CompanySerializer(company)
    return Response(data=serializer.data, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_sign_up(request: Request) -> Response:
    username = request.data.get('username', '')
    email = request.data.get('email', '')
    user: User = User.objects.filter(username=username).first()

    if not user:
        user = User.objects.create(
            username=username,
            email=email
        )
        user.save()
        Token.objects.create(user=user).save()

    serializer = UserSerializer(user)
    return Response(data=serializer.data, status=200)
