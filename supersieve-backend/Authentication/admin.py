from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *


@admin.register(PermissionPattern)
class PermissionPattern(admin.ModelAdmin):
    list_display = ['module', 'method']


@admin.register(User)
class UserPanel(UserAdmin):
    model = User
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('profile', 'email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'mobile', 'created_by')}),

        (_('Address info'), {'fields': (
            'Address',)}),

        (_('Activation Status'), {
            'fields': (
                'is_active', 'is_phone_verified', 'is_email_verified', 'reason'),
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser',
                       'groups', 'user_permissions', 'permission'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'profile', 'full_name', 'mobile', 'is_staff', 'user_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email', 'mobile')
    ordering = ('date_joined',)
    required = ('first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions',)
