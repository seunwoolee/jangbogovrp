import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = "jangbogo.settings"
django.setup()

from company.models import Company
from customer.models import Order, Customer, MutualDistance
from mysql_service import DB


if __name__ == '__main__':
    mysql = DB()
    mutual_distances: list = mysql.get_mutual_distance()
    for mutual_distance in mutual_distances:
        try:
            start = Customer.objects.get(customer_id=mutual_distance['vd_guestId'])
            end = Customer.objects.get(customer_id=mutual_distance['vd_deguestId'])

            MutualDistance.objects.create(
                start=start,
                end=end,
                distance=mutual_distance['vd_distanceValue'],
            ).save()
        except Exception as e:
            print(e)
