from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient

from mssql_service import ERPDB
from mysql_service import DB


class DeliveryTest(TestCase):
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

    def test_get_delivery_list(self):
        data = {'startDate': '2020-09-01', 'endDate': '2020-09-03'}
        response: Response = self.drf_client.get('/delivery/deliveries/', data=data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, 200)

    def test_map_groups_view(self):
        data = {'routeMId': '653'}
        response: Response = self.drf_client.get('/delivery/map_groups/', data=data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, 200)

    def test_maps_view(self):
        data = {'routeM': 87}
        response: Response = self.drf_client.get('/delivery/maps/', data=data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, 200)