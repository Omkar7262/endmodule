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


class VendorCategory(BaseModel):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


Account_Type = [(1, "Saving"), (2, "Current")]


class Vendor(BaseModel):
    vendor_code = models.CharField(max_length=100, verbose_name="Vendor Code", null=True, blank=True)
    vendor_codeword = models.CharField(max_length=150, verbose_name="Vendor Codeword", null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name="First Name", blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name="Last Name", blank=True, null=True)
    category = models.ForeignKey(VendorCategory, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(
        "Product.Product",  # Lazy reference
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    email = models.EmailField(verbose_name="Email", unique=True, null=True, blank=True)
    mobile = models.CharField(verbose_name="Mobile", max_length=20, null=True, blank=True)
    address = models.TextField(verbose_name="Address", null=True, blank=True)
    gst = models.CharField(verbose_name="GST No", max_length=100, null=True, blank=True)
    gst_value = models.FloatField(verbose_name="GST Value", null=True, blank=True)
    ac_type = models.IntegerField(choices=Account_Type, verbose_name="Account Type", default=1)
    bn = models.CharField(max_length=15, verbose_name="Bank Name", null=True, blank=True)
    ahn = models.CharField(max_length=15, verbose_name="Account Holder Name", null=True, blank=True)
    ac_no = models.CharField(max_length=15, verbose_name="Account Number", null=True, blank=True)
    ifsc = models.CharField(max_length=12, verbose_name="IFSC Code", null=True, blank=True)
    upi = models.CharField(max_length=15, verbose_name="UPI id", null=True, blank=True)
    cn = models.CharField(max_length=256, verbose_name="Company Name", null=True, blank=True)
    is_igst = models.BooleanField(verbose_name="IS IGST", default=False)

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            last_vendor = Vendor.objects.order_by('-id').first()
            if last_vendor and last_vendor.vendor_code:
                last_code = int(last_vendor.vendor_code.split('-')[-1])
                self.vendor_code = f"VN-{last_code + 1:04d}"
            else:
                self.vendor_code = "VN-0001"
        super().save(*args, **kwargs)
