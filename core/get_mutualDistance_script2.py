import os
import django
from django.db.models import Q

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
            print(mutual_distance['vd_guestId'])

            start = Customer.objects.get(customer_id=mutual_distance['vd_guestId'])
            end = Customer.objects.get(customer_id=mutual_distance['vd_deguestId'])

            if MutualDistance.objects.filter(Q(start=start), Q(end=end)).first():
                continue


            MutualDistance.objects.create(
                start=start,
                end=end,
                distance=mutual_distance['vd_distanceValue'],
                json_map=mutual_distance['vd_jsonData'],
            ).save()
        except Exception as e:
            print(e)
