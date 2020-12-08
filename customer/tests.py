from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient

from mssql_service import ERPDB


class CustomerTest(TestCase):
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

    def test_preview_order_view(self):
        data = {'isAm': True}
        response: Response = self.drf_client.get('/customer/preview_order/', data=data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, 200)

    def test_get_orders_view(self):
        data = {'order_ids': [111,222,33]}
        response: Response = self.drf_client.get('/customer/get_orders/', data=data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, 200)

    def test_get_customer(self):
        data = {'customerCode': '574845'}
        response: Response = self.drf_client.get('/customer/get_customer/', data=data)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.status_code, 200)