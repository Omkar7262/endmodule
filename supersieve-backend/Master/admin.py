from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(InvoiceSetting)
class InvoiceSettingAdmin(admin.ModelAdmin):
    list_display = ['prefix']
