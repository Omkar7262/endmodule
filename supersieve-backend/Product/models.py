import uuid
from django.db import models
from django.utils import timezone
from django.apps import apps


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey("Authentication.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class Package(BaseModel):
    pck_name = models.CharField(max_length=100, verbose_name="Package Name", null=True, blank=True)
    weight = models.FloatField(default=0, null=True, blank=True, verbose_name="Weight")
    color = models.CharField(max_length=50, verbose_name="Color", null=True, blank=True)

    def __str__(self):
        return f"{self.pck_name}"


class Material(BaseModel):
    category = models.ForeignKey(
        "Vendor.VendorCategory",  # Lazy reference
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    mn = models.CharField(max_length=50, verbose_name="Material Name")

    def __str__(self):
        return f"{self.mn}"


class ProductType(BaseModel):
    pt = models.CharField(max_length=50, verbose_name="Product Type")

    def __str__(self):
        return f"{self.pt}"


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    pt = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=True)
    gauge = models.CharField(max_length=50, verbose_name="Gauge", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class RawMaterial(BaseModel):
    mat_name = models.CharField(max_length=100, verbose_name="Raw Material Name", null=True, blank=True)

    def __str__(self):
        return f"{self.mat_name}"
    # size = models.CharField(max_length=50, verbose_name="Size", null=True, blank=True)
    # weight = models.CharField(max_length=50, verbose_name="Weight", null=True, blank=True)
    # roll = models.CharField(max_length=50, verbose_name="Roll", null=True, blank=True)
    #
    # def __str__(self):
    #     return f"{self.name}"
