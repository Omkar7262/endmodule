# Generated by Django 5.1 on 2024-10-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0002_vendor_ac_type_vendor_address_vendor_gst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='ac_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Saving'), (2, 'Current')], null=True, verbose_name='Account Type'),
        ),
    ]
