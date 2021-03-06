from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from company.models import Company, Driver
from company.serializers import CompanySerializer, UserSerializer, DriverSerializer


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


@api_view(['POST'])
def create_driver(request: Request) -> Response:
    username = request.data.get('name', '')
    course_number = request.data.get('courseNumber', '')
    company_code = request.data.get('company', '0')

    if User.objects.filter(username=username).first():
        return Response(data={"message": "동일한 이름의 기사가 있습니다. 다른 이름으로 저장해주세요"}, status=400)

    user = User.objects.create(username=username)
    user.set_password('123')
    user.save()

    Token.objects.create(user=user).save()

    driver = Driver.objects.create(
        user=user,
        name=username,
        course_number=course_number
    )

    if company_code != '0':
        company = Company.objects.get(code=company_code)
        driver.company = company

    driver.save()

    return Response(status=200)


@api_view(['DELETE'])
def delete_driver(request: Request) -> Response:
    driver_id = request.data.get('id', '')
    driver = Driver.objects.get(id=driver_id)
    driver.user.delete()
    return Response(status=200)


@api_view(['GET'])
def get_drivers(request: Request) -> Response:
    drivers = Driver.objects.all()
    serializer = DriverSerializer(drivers, many=True)
    return Response(data=serializer.data, status=200)


@api_view(['POST'])
def create_push_key(request: Request) -> Response:
    push_key = request.data.get('pushKey', "")
    user: User = request.user
    driver: Driver = user.driver.first()
    assert driver is not None, "driver does not exists"

    driver.push_key = push_key
    driver.save()
    return Response(status=200)
