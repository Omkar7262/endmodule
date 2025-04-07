from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Serializers import PurchaseOrderSerializers
from .models import PurchaseOrder


class PurchaseOrderView(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializers
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        unit = serializer.validated_data.get("unit", 0)
        rate_unit = serializer.validated_data.get("rate_unit", 0)
        net_value = unit * rate_unit
        serializer.save(net_value=net_value)
