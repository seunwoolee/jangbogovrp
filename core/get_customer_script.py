import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = "jangbogo.settings"
django.setup()

from customer.models import Customer
from mysql_service import DB

if __name__ == '__main__':
    mysql = DB()
    customers: list = mysql.get_customers()
    for customer in customers:
        try:
            Customer.objects.create(
                customer_id=customer['vg_guestId'],
                name=customer['vg_guestName'],
                address=customer['vg_guestJuso'],
                latitude=customer['vg_guestLat'],
                longitude=customer['vg_guestLon'],
            ).save()
        except Exception as e:
            print(e)
