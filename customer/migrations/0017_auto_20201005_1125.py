# Generated by Django 3.1.1 on 2020-10-05 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_remove_routed_orders'),
        ('customer', '0016_order_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='route_orders', to='delivery.routed'),
        ),
    ]