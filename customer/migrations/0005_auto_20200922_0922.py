# Generated by Django 3.1.1 on 2020-09-22 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_mutualdistance_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='altitude',
            new_name='longitude',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
    ]
