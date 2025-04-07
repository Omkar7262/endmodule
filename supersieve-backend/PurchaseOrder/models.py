import uuid
from django.utils import timezone

from django.db import models

from Vendor.models import Vendor


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey("Authentication.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class PurchaseOrder(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_orders",
                               verbose_name="Vendor")
    po_no = models.IntegerField(default=0, verbose_name="P.O. No", null=True, blank=True)
    po_date = models.DateField(verbose_name="P.O. Date", null=True, blank=True)
    amd_no = models.IntegerField(default=0, verbose_name="Amendment No", blank=True, null=True)
    amd_date = models.DateField(verbose_name="Date", null=True, blank=True)
    issued_by = models.CharField(max_length=256, verbose_name="Issued By", null=True, blank=True)
    val_start_dat = models.DateField(verbose_name="Validity Start Date", null=True, blank=True)
    val_end_dat = models.DateField(verbose_name="Validity End Date", null=True, blank=True)
    gst_no = models.CharField(max_length=100, verbose_name="GST Registration Number", null=True, blank=True)
    pan_no = models.CharField(max_length=20, verbose_name="PAN Number", null=True, blank=True)
    deliver_to = models.TextField(verbose_name="Please Deliver to", null=True, blank=True)
    del_term = models.CharField(max_length=150, null=True, blank=True, verbose_name="Delivery Term")
    pay_term = models.CharField(max_length=256, verbose_name="Payment Term", null=True, blank=True)
    doc_crn = models.CharField(max_length=10, verbose_name="Document Currency", null=True, blank=True)
    sr_no = models.CharField(max_length=10, verbose_name="SNo", null=True, blank=True)
    ic = models.CharField(max_length=100, verbose_name="Item Code / HSN Code", null=True, blank=True)
    des = models.TextField(verbose_name="Description", null=True, blank=True)
    order_qty = models.IntegerField(default=0, verbose_name="Order Qty", null=True, blank=True)
    unit = models.IntegerField(default=0, verbose_name="Unit", null=True, blank=True)
    rate_unit = models.FloatField(default=0, verbose_name="Rate Per Unit", null=True, blank=True)
    net_value = models.FloatField(default=0, verbose_name="Net Value", null=True, blank=True)
