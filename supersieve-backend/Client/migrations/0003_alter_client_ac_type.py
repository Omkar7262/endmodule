# Generated by Django 5.1 on 2024-10-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0002_client_ac_type_client_address_client_gst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='ac_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Saving'), (2, 'Current')], null=True, verbose_name='Account Type'),
        ),
    ]
