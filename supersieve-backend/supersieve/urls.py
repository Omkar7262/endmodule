from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Authentication.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.routers import DefaultRouter
from Master.views import InvoiceSettingView
from Client.views import ClientView
from InventoryManagement.views import InventoryView
from Product.views import MaterialView, ProductTypeView, ProductView, PackageView, RawMaterialView
from PurchaseOrder.views import PurchaseOrderView
from Vendor.views import VendorCategoryView, VendorView

router = DefaultRouter()
router.register('mt', MaterialView, basename="material")
router.register('pt', ProductTypeView, basename="product type")
router.register('pd', ProductView, basename="product")
router.register('vnc', VendorCategoryView, basename="vendor category")
router.register('vn', VendorView, basename="vendor")
router.register('clt', ClientView, basename="client")
router.register('pck', PackageView, basename="package")
router.register('ins', InvoiceSettingView, basename="invoice setting view")
router.register('rawmat', RawMaterialView, basename="Raw Material")
router.register('po', PurchaseOrderView, basename="purchase order")
router.register('im', InventoryView, basename="Inventory management")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('api/login', Login.as_view()),
    path('refreshToken', TokenRefreshView.as_view()),
    path('api/verify/', TokenVerifyView.as_view()),
    path('', include(router.urls))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
