from django.contrib import admin
from .models import Material, ProductType, Product, Package, RawMaterial


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['mn']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['pt']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['pck_name']


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ['mat_name']
