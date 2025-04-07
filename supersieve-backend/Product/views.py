from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Serializers import MaterialSerializers, ProductTypeSerializers, ProductSerializers, PackageSerializers, \
    RawMaterialSerializers
from .models import Material, ProductType, Product, Package, RawMaterial


class MaterialView(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)


class ProductTypeView(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def get_queryset(self):
        """
        Override to filter products by VendorCategory UID.
        """
        vendor_category_id = self.request.query_params.get('vendor_category_id')
        if vendor_category_id:
            return Product.objects.filter(
                material__category__id=vendor_category_id
            )
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)


class PackageView(ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)


class RawMaterialView(ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializers
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"
    http_method_names = ['post', 'put', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        return super().create(request, *args, **kwargs)


