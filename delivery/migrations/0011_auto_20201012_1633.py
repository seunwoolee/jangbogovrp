# Generated by Django 3.1.1 on 2020-10-12 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0010_auto_20201005_1425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='routed',
            options={'ordering': ['route_number', 'route_index', 'id']},
        ),
    ]