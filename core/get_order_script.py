import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = "jangbogo.settings"
django.setup()

from company.models import Company
from customer.models import Order, Customer
from mysql_service import DB


if __name__ == '__main__':
    mysql = DB()
    orders: list = mysql.get_orders()

    # orders: list = mysql.get_chilseong_orders()

    # Order.objects.all().delete()

    for order in orders:
        location_id = '00' + str(order['ve_locationId'])
        customer = Customer.objects.filter(customer_id=order['ve_guestId']).first()
        company = Company.objects.get(code=location_id)
        if order['ve_meridiemType'] == '0':
            is_am = True
        else:
            is_am = False

        try:
            Order.objects.create(
                order_id=order['ve_accno'],
                company=company,
                date=order['ve_deliveryDate'],
                customer=customer,
                is_am=is_am,
                price=order['ve_pay'],
            ).save()
        except Exception as e:
            print(e)
