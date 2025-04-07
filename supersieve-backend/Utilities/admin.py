from django.contrib import admin
from Utilities.models import PurchaseOrder, Inventory, SpareParts


@admin.register(PurchaseOrder)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['order_name']


@admin.register(Inventory)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(SpareParts)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
