# Generated by Django 3.1.1 on 2020-10-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0017_auto_20201005_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='course_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
