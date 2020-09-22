# Generated by Django 3.1.1 on 2020-09-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='altitude',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='latitude',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
