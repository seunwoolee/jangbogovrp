from django.contrib import admin

from customer.models import Customer, Order, MutualDistance

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(MutualDistance)
