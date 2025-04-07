from rest_framework import serializers
from .models import *


class InvoiceSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceSetting
        fields = '__all__'
