from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import InvoiceSettingSerializer
from .models import InvoiceSetting


# Create your views here.

class InvoiceSettingView(ModelViewSet):
    queryset = InvoiceSetting.objects.all()
    serializer_class = InvoiceSettingSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uid'

    # http_method_names = ['post', 'put', 'delete', 'get']

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['updated_by'] = request.user.pk
        return super().update(request, *args, **kwargs)
