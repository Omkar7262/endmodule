from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Serializers import ClientSerializers
from .models import Client


class ClientView(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)
