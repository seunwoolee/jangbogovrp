# Generated by Django 3.1.1 on 2020-09-22 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_order_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(),
        ),
    ]
