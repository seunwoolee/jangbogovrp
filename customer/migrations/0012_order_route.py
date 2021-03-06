# Generated by Django 3.1.1 on 2020-09-29 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_remove_routed_orders'),
        ('customer', '0011_mutualdistance_json_map'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='route',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='delivery.routed'),
            preserve_default=False,
        ),
    ]
