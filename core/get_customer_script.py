import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = "jangbogo.settings"
django.setup()

from customer.models import Customer
from mysql_service import DB

if __name__ == '__main__':
    mysql = DB()

    # Customer.objects.all().delete()

    customers: list = mysql.get_customers()

    for customer in customers:
        if Customer.objects.filter(customer_id=customer['vg_guestId']).first():
            continue

        try:
            Customer.objects.create(
                customer_id=customer['vg_guestId'],
                name=customer['vg_guestName'],
                address=customer['vg_guestJuso'].strip(),
                latitude=customer['vg_guestLat'],
                longitude=customer['vg_guestLon'],
            ).save()
        except Exception as e:
            print(e)
