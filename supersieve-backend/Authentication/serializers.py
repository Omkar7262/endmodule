import json
import random
from rest_framework import serializers
# import masterdata.models
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken, api_settings, PasswordField
from django.contrib.auth.models import update_last_login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.template.loader import get_template
from rest_framework.status import *
from rest_framework import exceptions
from .helper import *
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


def user_message(user):
    message = {
        'full_name': user.full_name(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
        'site_name': 'LockTrust',
        # 'site_url': settings.MAIN_URL
    }
    return message


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile', 'full_name', 'email', 'mobile', 'uid', 'userType', 'sub_user',
                  "is_email_verified"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    code_token = serializers.CharField(max_length=255)
    code = serializers.IntegerField()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(write_only=True, required=False)
        self.fields["password"] = PasswordField(required=False)

    def validate(self, attrs):
        uidb64, token = attrs.get('code_token').split("/")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if user.phone_otp == attrs.get('code'):
                if user.expiry_phone_otp <= timezone.now():
                    error_name = "Invalid OTP"
                    error_message = "One Time Password has expired"
                    raise exceptions.AuthenticationFailed(error_message, error_name)
                else:
                    user.is_phone_verified = True
                    user.is_active = True
                    user.save()
            else:
                error_name = "Invalid OTP"
                error_message = "The one time password you have Entered is not Correct Please Enter the Correct One " \
                                "Time Password"
                raise exceptions.AuthenticationFailed(error_message, error_name)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and generate_token.check_token(user, token):
            data = dict()
            refresh = self.get_token(user)
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
            data['userData'] = ProfileSerializer(user).data

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)
            return data
        else:
            raise ValidationError({"token": "token has expired"})


class UserRegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile']

    def create(self, validated_data):
        # if validated_data['password'] != validated_data['password2']:
        #     raise exceptions.ValidationError({"password2": "Password and Confirmed password are not equal"})
        # elif validated_data['password'] == "" or validated_data['password2'] == "":
        #     raise exceptions.ValidationError({"password2": "Password and Confirmed password can not empty"})
        otp = random.randint(100000, 999999)
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile=validated_data['mobile'],
            # user_type=validated_data['user_type'],
            phone_otp=otp,
            expiry_phone_otp=setExpiryDateTimeForOTP(),
        )
        # user.set_password(validated_data['password'])
        # user.save()
        # send_otp_twilio(otp, user.mobile)
        return Response({"message": "One time password has sent on Mobile"}, status=HTTP_201_CREATED)


class AllCreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'mobile', 'email', 'first_name', 'last_name', 'user_type', 'date_joined', 'uid')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'mobile': {'required': True},
            'user_type': {'required': True}
        }

    def create(self, validated_data):
        user_request = self.context['request'].user
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile=validated_data['mobile'],
            user_type=validated_data['user_type'],
            created_by=self.context['request'].user
        )

        # user.country_code = validated_data['country_code'] if validated_data.get('country_code') else ""
        # user.company_name = validated_data['company_name'] if validated_data.get('company_name') else ""
        user.created_by = user_request
        user.set_password(uuid.uuid4().hex[:8])
        user.save()
        # message = user_message(user)
        # send_email(message, 'Activate Email', validated_data['email'], 'email/activate_account.html',
        #            'email/activate_account.txt')
        return user


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'mobile', 'email', 'first_name', 'last_name', 'user_type', 'uid')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'mobile': {'required': True},
            'user_type': {'required': True},

        }

    def create(self, validated_data):
        user_request = self.context['request'].user
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile=validated_data['mobile'],
            user_type=validated_data['user_type'],

            Address=validated_data['Address'],
            city=validated_data['city'],

            created_by=self.context['request'].user
        )

        # user.country_code = validated_data['country_code'] if validated_data.get('country_code') else ""
        # user.company_name = validated_data['company_name'] if validated_data.get('company_name') else ""
        user.created_by = user_request
        # user.set_password(uuid.uuid4().hex[:8])
        # user.save()
        # message = user_message(user)
        # send_email(message, 'Activate Email', validated_data['email'], 'email/activate_account.html',
        #            'email/activate_account.txt')
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=12, read_only=True)

    class Meta:
        model = User
        fields = ['uid', 'email', 'first_name', 'last_name', 'email', 'mobile', 'role']


class TokenAuthenticationUserSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class VendorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            'uid', 'first_name', 'last_name', 'email', 'password', 'mobile',
            'gst', 'cn', 'address', 'contact_info', 'at', 'bn', 'ahn',
            'ac_no', 'ifsc', 'upi'
        )

    def create(self, validated_data):
        user_request = self.context['request'].user
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, user_type=2,
                                        created_by=user_request
                                        )
        user.set_password(password)
        user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('uid', 'first_name', 'last_name', 'email', 'password', 'mobile', 'gst',
                  'cn', 'address', 'contact_info', 'at', 'bn', 'ahn', 'ac_no', 'ifsc', 'upi')

    def create(self, validated_data):
        user_request = self.context['request'].user
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, user_type=3,
                                        created_by=user_request
                                        )
        user.set_password(password)
        user.save()
        return user
