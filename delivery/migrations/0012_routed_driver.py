# Generated by Django 3.1.1 on 2020-11-11 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_driver'),
        ('delivery', '0011_auto_20201012_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='routed',
            name='driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='company.driver'),
        ),
    ]