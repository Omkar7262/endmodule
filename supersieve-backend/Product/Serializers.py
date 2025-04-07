from rest_framework import serializers
from .models import Material, ProductType, Product, Package, RawMaterial


class MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class ProductTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class PackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class RawMaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = "__all__"
