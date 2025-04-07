from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Serializers import InventorySerializers
from .models import Inventory


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)
