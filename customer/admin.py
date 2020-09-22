from django.contrib import admin

from customer.models import Customer, Order, MutualDistance


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ["id"]
    search_fields = ["id", "name", "address"]


@admin.register(Order)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ["date", "is_am"]
    search_fields = ["customer__name"]


# @admin.register(MutualDistance)
# class CustomerAdmin(admin.ModelAdmin):
#     list_filter = ["id"]
#     search_fields = ["start__name", "end__name"]

admin.site.register(MutualDistance)


