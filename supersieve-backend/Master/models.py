import uuid
from django.db import models
from django.utils import timezone

invoicenoType = [(1, "sequence"), (2, "Random")]


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey("Authentication.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class InvoiceSetting(BaseModel):
    invoiceNoType = models.IntegerField(choices=invoicenoType,verbose_name="Invoice Number Type", help_text="Invoice Number Type", default=0)
    prefix = models.CharField(max_length=50, verbose_name="Invoice Prefix", help_text="Invoice Prefix")
    notes = models.TextField(verbose_name="Invoice Notes", help_text="Invoice Notes", null=True)
    terms = models.TextField(verbose_name="Invoice Terms", help_text="Invoice Terms", null=True)
    sign = models.ImageField(upload_to='uploads/invoice/', verbose_name="Invoice Sign", help_text="Invoice Sign",
                             null=True)
    logo = models.ImageField(upload_to='uploads/invoice/', verbose_name="Invoice Image", help_text="Invoice Image",
                             null=True)
