from rest_framework import serializers
from .models import VendorCategory, Vendor


class VendorCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorCategory
        fields = "__all__"


class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
