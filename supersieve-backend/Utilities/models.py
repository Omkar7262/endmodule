from django.db import models


class PurchaseOrder(models.Model):
    order_name = models.CharField(max_length=50, verbose_name="Order Name")
    inward = models.CharField(max_length=50, verbose_name="Inward", null=True, blank=True)
    outward = models.CharField(max_length=50, verbose_name="Outward", null=True, blank=True)


class Inventory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Product Name")


class SpareParts(models.Model):
    name = models.CharField(max_length=50, verbose_name="Spare Part name")

