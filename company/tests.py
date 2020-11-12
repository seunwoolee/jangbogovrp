from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient

from company.models import Driver


class CompanyTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='admin')
        self.user.set_password('admin')
        self.user.first_name = '이승우'
        self.user.save()

        response = self.client.post('/rest-auth/login/', data={
            "username": "admin",
            "password": "admin",
        })

        self.token: str = response.data['key']

        self.drf_client = APIClient()
        self.drf_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_kakao_sign_up(self):
        data = {'username': 'a1a2a3a4a6', 'email': 'leemoney93@daum.net'}
        response: Response = self.drf_client.post('/company/kakao_sign_up/', data)
        self.assertEqual(response.status_code, 200)

    def test_driver(self):
        data = {'name': '이승우', 'courseNumber': 1}
        response: Response = self.drf_client.post('/company/create_driver/', data)
        self.assertEqual(response.status_code, 200)

        data = {'name': '이승우', 'courseNumber': 1}
        response: Response = self.drf_client.post('/company/create_driver/', data)
        self.assertEqual(response.status_code, 400)

        data = {'name': '이승우반야월', 'courseNumber': 1, 'company_code': '011'}
        response: Response = self.drf_client.post('/company/create_driver/', data)
        self.assertEqual(response.status_code, 200)

        driver = Driver.objects.filter().first()
        data = {'id': driver.id}
        response: Response = self.drf_client.delete('/company/delete_driver/', data)
        self.assertEqual(response.status_code, 200)

        data = {'name': '이승우', 'courseNumber': 1}
        response: Response = self.drf_client.post('/company/create_driver/', data)
        self.assertEqual(response.status_code, 200)

        response: Response = self.drf_client.get('/company/get_drivers/')
        self.assertEqual(response.status_code, 200)
