import uuid
from django.utils import timezone
from django.db import models
from Product.models import Product, Package, RawMaterial
from Vendor.models import Vendor


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey("Authentication.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class Inventory(BaseModel):
    UNIT_CHOICES = [
        ('F', 'Feet'),
        ('M', 'Meters'),
    ]
    raw_mat = models.ForeignKey(RawMaterial, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="Raw Material")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vendor")
    video_upload = models.FileField(upload_to="uploads/videos/", null=True, blank=True)
    image = models.ImageField(upload_to="uploads/images", null=True, blank=True)
    invoice_weight = models.CharField(max_length=100, verbose_name="Invoice Weight", null=True, blank=True)
    actual_weight = models.CharField(max_length=100, verbose_name="Actual Weight", null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Package Name")
    package_weight = models.FloatField(default=0, verbose_name="Package Weight", null=True, blank=True)
    len_a = models.FloatField(verbose_name="Size 1", null=True, blank=True)
    len_a_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="Size 1 unit", default='feet')
    len_b = models.FloatField(verbose_name="Size 2", null=True, blank=True)
    len_b_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="Size 2 unit", default='feet')
    sqft_value = models.CharField(max_length=50, verbose_name="Square feet Value", null=True, blank=True)

    def convert_to_square_feet(self):
        if self.len_a is not None and self.len_b is not None:
            # Convert len_a to feet if it's in meters
            if self.len_a_unit == 'M':
                len_a_feet = self.len_a * 3.28084
            else:
                len_a_feet = self.len_a

            # Convert len_b to feet if it's in meters
            if self.len_b_unit == 'M':
                len_b_feet = self.len_b * 3.28084
            else:
                len_b_feet = self.len_b

            # Calculate the square feet
            square_feet = len_a_feet * len_b_feet
            self.sqft_value = f"{square_feet:.2f} sq ft"

    def save(self, *args, **kwargs):
        # Call the conversion method before saving
        self.convert_to_square_feet()
        super().save(*args, **kwargs)
