from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Serializers import VendorCategorySerializers, VendorSerializers
from .models import VendorCategory, Vendor


class VendorCategoryView(ModelViewSet):
    queryset = VendorCategory.objects.all()
    serializer_class = VendorCategorySerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)


class VendorView(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)
