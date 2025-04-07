from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings
from twilio.rest import Client
# from faker import Faker
from django.db.models.signals import pre_save
from django.dispatch import receiver

authProcess = ((1, "SignUp"),
               (2, "Login"))

# duration = ((1, 'Daily'),
#             (2, 'Weekly'),
#             (3, 'Bi-weekly'),
#             (4, 'Monthly'))

METHOD = [
    ('create', 'Create'),
    ('update', 'Update'),
    ('view', 'View'),
    ('delete', 'Delete')
]

userType = [(1, 'Admin'),
            (2, 'Vendor'),
            (3, 'Client'),
            ]

Account_Type = [(1, 'Saving'),
                (2, 'Current'),
                ]


class CommonField(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class PermissionPattern(CommonField):
    module = models.CharField(max_length=30, verbose_name='Module')
    method = models.CharField(max_length=30, verbose_name='Component', choices=METHOD)
    user_type = models.IntegerField(
        verbose_name="User Type",
        blank=True,
        null=True,
        choices=userType,
        default=1,

    )

    def __str__(self):
        return f"{self.method}_{self.module}"


def setExpiryDateTimeForOTP():
    return timezone.now() + timezone.timedelta(minutes=10)


def setSuperUser():
    user = User.objects.filter(is_superuser=True).first()
    return user


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user

    @staticmethod
    def send_otp(otp, mobile):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=f'Your one time password is {otp}',
                                         from_=settings.TWILIO_PHONE_NO,
                                         to=mobile)
        print(message.sid)


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    profile = models.FileField(
        verbose_name="Profile",
        upload_to="profile",
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=20, blank=True,
                                  null=True)
    last_name = models.CharField(max_length=20, blank=True,
                                 null=True)
    display_name = models.CharField(max_length=255, blank=True)
    Address = models.TextField(null=True, blank=True)

    email = models.EmailField(
        verbose_name="Email",
        unique=True, null=True, blank=True
    )
    mobile = models.CharField(
        verbose_name="Mobile",
        max_length=20, null=True, blank=True

    )
    city = models.CharField(
        verbose_name="City",
        max_length=25,
        blank=True,
        null=True
    )
    user_type = models.IntegerField(
        verbose_name="User Type",
        blank=True,
        null=True,
        choices=userType,
        default=1
    )
    contact_info = models.JSONField(verbose_name="Contact Info", max_length=255, blank=True, null=True)
    created_by = models.ForeignKey("User", on_delete=models.SET(setSuperUser), blank=True, null=True,
                                   related_name="created_by_user")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True, verbose_name="User Block Reason")
    phone_otp = models.IntegerField(blank=True, null=True)
    expiry_phone_otp = models.DateTimeField(default=timezone.now)
    email_otp = models.IntegerField(blank=True, null=True)
    expiry_email_otp = models.DateTimeField(default=timezone.now)
    gst = models.CharField(max_length=256, verbose_name="GST", null=True, blank=True)
    permission = models.ManyToManyField(PermissionPattern, verbose_name='user_permission', blank=True)
    cn = models.CharField(max_length=256, verbose_name="Company Name", null=True, blank=True)
    address = models.TextField(verbose_name="Address", null=True, blank=True)
    at = models.IntegerField(choices=Account_Type, verbose_name="Account Type", null=True, blank=True)
    bn = models.CharField(max_length=50, verbose_name="Bank Name", null=True, blank=True)
    ahn = models.CharField(max_length=50, verbose_name="Account Holder Name", null=True, blank=True)
    ac_no = models.CharField(max_length=15, verbose_name="Account Number", null=True, blank=True)
    ifsc = models.CharField(max_length=50, verbose_name="IFSC Code", null=True, blank=True)
    upi = models.CharField(max_length=50, verbose_name="UPI id", null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile', 'user_type']
    EMAIL_FIELD = 'email'

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def userType(self):
        for i in userType:
            if self.user_type == i[0]:
                return i[1].lower()
        return f"{self.user_type}"

    def role(self):
        for i in userType:
            if i[0] == self.user_type:
                return i[1].lower()


class OneTimePassword(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="onetimepassword_user")
    one_time_password_for_mobile = models.IntegerField(blank=True, null=True)
    one_time_password_for_email = models.IntegerField(blank=True, null=True)
    process = models.IntegerField(default=1, choices=authProcess)
    expiryDate = models.DateTimeField(default=setExpiryDateTimeForOTP)


# class PermissionPattern(CommonField):
#     module = models.CharField(max_length=30, verbose_name='Module')
#     method = models.CharField(max_length=30, verbose_name='Component', choices=METHOD)
#     user_type = models.IntegerField(
#         verbose_name="User Type",
#         blank=True,
#         null=True,
#         choices=userType,
#         default=1,
#
#     )
#
#     def __str__(self):
#         return f"{self.method}_{self.module}"
#
#     @property
#     def codename(self):
#         return f"{self.method}_{self.module}"


class UserRole(CommonField):
    rn = models.CharField(max_length=50, verbose_name='User Role Name', help_text="Role Name", null=True)
    pur = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, verbose_name='Parent User Role',
                            help_text="Parent User Role Name", null=True)
    up = models.ManyToManyField(PermissionPattern, verbose_name='user_permission')

    def __str__(self):
        return self.rn

    def user_permissions(self):
        return ",".join([x.module for x in self.up.all()])
