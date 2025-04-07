from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import auth
from rest_framework import viewsets
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
import string
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.exceptions import *
from .helper import *
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication


def GenerateOTP():
    return random.randint(1000, 9999)


def randomPasswordGenerator():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(8))
    return password


class SignupAPI(APIView):

    @transaction.atomic
    def post(self, request):
        fm = UserRegistrationSerializer(data=request.data)
        if fm.is_valid():
            fm.save()
            return Response({"message": "One time password has sent on Mobile"},
                            status=HTTP_201_CREATED)
        else:
            return Response(fm.errors, status=HTTP_400_BAD_REQUEST)


class resendOTPOnmessage(APIView):

    @transaction.atomic
    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(mobile=body['mobile'])
            otp = self.getOTP(user)
            if not user.is_phone_verified:
                send_otp_by_plivo(otp, user.mobile)

        except User.DoesNotExist:
            error_name = "Invalid User"
            error_message = "User doesnot exist"
            raise AuthenticationFailed(error_message, error_name)
        return HttpResponse("Accepted", status=HTTP_202_ACCEPTED)

    @staticmethod
    def getOTP(user):
        res_message = random.randint(100000, 999999)
        otp = OneTimePassword(user=user,
                              one_time_password_for_mobile=res_message)
        otp.save()

        return {"message": res_message}


class resendOTPOncall(APIView):

    @transaction.atomic
    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(mobile=body['mobile'])
            otp = self.getOTP(user)
            if not user.is_phone_verified:
                call_for_otp_by_twilio(otp, user.mobile)

        except User.DoesNotExist:
            error_name = "Invalid User"
            error_call = "User doesnot exist"
            raise AuthenticationFailed(error_call, error_name)
        return HttpResponse("Accepted", status=HTTP_202_ACCEPTED)

    @staticmethod
    def getOTP(user):
        res_call = random.randint(100000, 999999)
        otp = OneTimePassword(user=user,
                              one_time_password_for_mobile=res_call)
        otp.save()

        return {"call": res_call}


class ChangeMobileNo(APIView):

    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(mobile=body['new_mobile'])
            if user:
                error_name = "mobile"
                error_message = "User already exist with new Mobile Number"
                raise ValidationError({error_name: error_message})
        except User.DoesNotExist:
            pass
        try:
            user = User.objects.get(mobile=body['old_mobile'])
            user.mobile = body['new_mobile']
            user.save()
            otp = self.getOTP(user)

            if not user.is_phone_verified:
                send_otp_by_plivo(otp, user.mobile)

        except User.DoesNotExist:
            error_name = "Invalid User"
            error_message = "User doesnot exist"
            raise ValidationError({error_name: error_message})
        except Exception as e:
            raise e
        return Response({"message": "change"}, status=HTTP_202_ACCEPTED)

    @staticmethod
    def getOTP(user):
        res_call = random.randint(100000, 999999)
        otp = OneTimePassword(user=user,
                              one_time_password_for_mobile=res_call)
        otp.save()

        return {"call": res_call}


class ChangeEmail(APIView):

    @transaction.atomic
    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(email=body['old_email'])
            user.email = body['new_email']
            user.save()
            otp = self.getOTP(user)

            if not user.is_email_verified:
                send_email_otp(user.full_name, otp, user.email)

        except User.DoesNotExist:
            error_name = "Invalid User"
            error_message = "User doesnot exist"
            raise AuthenticationFailed(error_message, error_name)
        return Response({"message": "Email has changed"}, status=HTTP_202_ACCEPTED)

    @staticmethod
    def getOTP(user):
        res_email = random.randint(100000, 999999)
        otp = OneTimePassword(user=user,
                              one_time_password_for_email=res_email)
        otp.save()

        return {"email": res_email}


class resendOTPOnEmail(APIView):

    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(email=body['email'])
            otp = random.randint(100000, 999999)
            user.email_otp = otp
            user.expiry_email_otp = setExpiryDateTimeForOTP()
            user.save()
            if not user.is_email_verified:
                send_email_otp(user.full_name, otp, user.email)

        except User.DoesNotExist:
            error_name = "Invalid User"
            error_message = "User doesnot exist"
            raise AuthenticationFailed(error_message, error_name)
        return Response({"email": body['email']}, status=HTTP_202_ACCEPTED)


class SendOTPView(APIView):

    @transaction.atomic
    def post(self, request, uidb64, token):
        User = get_user_model()
        attempt = request.data['attempt']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and generate_token.check_token(user, token):
            try:
                user.is_email_verified = True
                user.save()
                otp = GenerateOTP()
                if attempt == 1:
                    send_otp_twilio(otp, user.mobile)
                elif attempt == 2:
                    send_otp_by_plivo(otp, user.mobile)
                elif attempt == 3:
                    call_for_otp_by_twilio(otp, user.mobile)
                message = user_message(user)
                return Response({"message": "otp has sent on your mobile number"}, status=HTTP_202_ACCEPTED)

            except User.DoesNotExist:
                error_name = "Invalid User"
                error_password = "User doesnot exist"
                raise AuthenticationFailed(error_password, error_name)


class VerifyMobile(APIView):

    @transaction.atomic
    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(mobile=body['mobile'])
            if user.phone_otp == int(body['otp']):
                if user.expiry_phone_otp <= timezone.now():
                    error_name = "Invalid OTP"
                    error_message = "One Time Password has expired"
                    raise AuthenticationFailed({error_name: error_message})
                user.is_phone_verified = True
                user.is_active = True
                user.save()
            else:
                error_name = "Invalid OTP"
                error_message = "OTP is either invalid or expired"
                raise AuthenticationFailed({error_name: error_message})
        except User.DoesNotExist:
            error_name = "Invalid User"
            error_message = "User doesnot exist"
            raise AuthenticationFailed({error_name: error_message})
        return HttpResponse("Accepted", status=HTTP_202_ACCEPTED)


class VerifyEmail(APIView):

    @transaction.atomic
    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(email=body['email'])
            if user.email_otp == int(body['otp']):
                if user.expiry_email_otp <= timezone.now():
                    error_name = "Invalid OTP"
                    error_message = "One Time Password has expired"
                    raise AuthenticationFailed(error_message, error_name)
                user.is_email_verified = True
                user.save()
                if user.is_phone_verified and user.is_email_verified:
                    user.is_active = True
                    user.save()
            else:
                error_name = "Invalid OTP"
                error_message = "OTP is either invalid or expired"
                raise exceptions.AuthenticationFailed(error_message, error_name)
        except User.DoesNotExist:
            error_name = "Invalid User"
            error_message = "User doesnot exist"
            raise exceptions.AuthenticationFailed(error_message, error_name)
        return Response({"message": "Accepted"}, status=HTTP_202_ACCEPTED)


def LogOut(request):
    auth.logout(request)
    return redirect("/")


class Login1(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=request.user.id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


class ResetPassword(APIView):

    @transaction.atomic
    def post(self, request):
        body = request.data
        try:
            user = User.objects.get(email=body['email'])
            if not user.is_active:
                raise AuthenticationFailed("Please activate your account", "User activation")
            message = user_message(user)
            send_email(message, 'Reset Password you account', user.email, 'Email/ResetPassword'
                                                                          '/resetpassword.html',
                       'Email/ResetPassword/resetpassword.txt')
            return Response({"message": "Reset link has sent on your Email"}, status=HTTP_202_ACCEPTED)

        except User.DoesNotExist:
            error_name = "Invalid User"
            error_password = "User doesnot exist"
            raise AuthenticationFailed(error_password, error_name)


class NewPasswordSetup(APIView):

    @transaction.atomic
    def post(self, request, uidb64, token):
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and generate_token.check_token(user, token):
            try:
                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    messages = {
                        'key': 'your password successfully reset'
                    }

                    return Response(messages, status=HTTP_202_ACCEPTED)

            except OneTimePassword.DoesNotExist:
                error_name = "Invalid OTP"
                error_message = "OTP is either invalid or expired"
                raise AuthenticationFailed(error_message, error_name)
            return redirect('login')
        else:
            raise ValidationError({"link": "Activation url has expired"})


class PasswordResetLink(auth_views.PasswordResetView):
    template_name = 'authentication/auth_recover.html'
    title = _('Password reset sent')
    extra_context = {"info": "Please check you email if not present check promotion or spam"}


class UserCreationApi(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AllCreateUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def create(self, request, *args, **kwargs):
        request_user = request.user
        request.data['created_by'] = request_user.pk
        instance = super(UserCreationApi, self).create(request, *args, **kwargs)
        return Response({"message": "User Created"}, status=HTTP_201_CREATED)


class CreateUserApi(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def create(self, request, *args, **kwargs):
        request_user = request.user
        request.data['created_by'] = request_user.pk
        instance = super(CreateUserApi, self).create(request, *args, **kwargs)
        user = User.objects.get(uid=instance.data['uid'])
        # update_permission(user)
        return Response({"message": "User Successfully Created"}, status=HTTP_201_CREATED)


class Login(TokenObtainPairView):
    serializer_class = TokenAuthenticationUserSerializer


class createUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "uid"

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user, is_deleted=False)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['created_by'] = request.user.pk
        return super(createUserView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = User.objects.get(uid=kwargs['uid'])
        request.data._mutable = True
        request.data['updated_by'] = request.user.pk
        request.data
        instance = super(createUserView, self).update(request, *args, **kwargs)
        message = {
            "message": "Data Updated"
        }
        return Response(message, status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_by = request.user
        instance.is_deleted = True
        instance.save()
        res = {'msg': 'Records Deleted Successfully'}
        return JsonResponse(res, safe=False)


class VendorManagement(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"

    def get_queryset(self):
        return self.queryset.filter(user_type=2, is_active=True)

    def create(self, request, *args, **kwargs):
        request.data['user_type'] = 2
        request.data['created_by'] = request.user
        instance = super().create(request, *args, **kwargs)
        return instance

    def update(self, request, *args, **kwargs):
        request.data['user_type'] = 2
        request.data['created_by'] = request.user
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            raise PermissionDenied({'message': 'You can\'t delete this user'})
        instance.is_active = False
        instance.is_block = False
        instance.save()
        return Response({"message": "User deleted successfully"}, status=HTTP_204_NO_CONTENT)

    def check_permissions(self, request):
        if request.user.is_anonymous:
            raise AuthenticationFailed({"message": "Authentication Required"})
        if self.action == "list" and request.user.permission.filter(module__iexact="vendor",
                                                                    method="view").count() >= 1:
            return True
        if self.action == "create" and request.user.permission.filter(module__iexact="vendor",
                                                                      method="create").count() >= 1:
            return True
        if self.action == "update" and request.user.permission.filter(module__iexact="vendor",
                                                                      method="update").count() >= 1:
            return True
        if self.action == "destroy" and request.user.permission.filter(module__iexact="vendor",
                                                                       method="delete").count() >= 1:
            return True
        return False


class ClientManagement(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = "uid"

    def get_queryset(self):
        return self.queryset.filter(user_type=3, is_active=True)

    def create(self, request, *args, **kwargs):
        request.data['user_type'] = 3
        request.data['created_by'] = request.user
        instance = super().create(request, *args, **kwargs)
        return instance

    def update(self, request, *args, **kwargs):
        request.data['user_type'] = 3
        request.data['created_by'] = request.user
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            raise PermissionDenied({'message': 'You can\'t delete this user'})
        instance.is_active = False
        instance.is_block = False
        instance.save()
        return Response({"message": "User deleted successfully"}, status=HTTP_204_NO_CONTENT)

    def check_permissions(self, request):
        if request.user.is_anonymous:
            raise AuthenticationFailed({"message": "Authentication Required"})
        if self.action == "list" and request.user.permission.filter(module__iexact="client",
                                                                    method="view").count() >= 1:
            return True
        if self.action == "create" and request.user.permission.filter(module__iexact="client",
                                                                      method="create").count() >= 1:
            return True
        if self.action == "update" and request.user.permission.filter(module__iexact="client",
                                                                      method="update").count() >= 1:
            return True
        if self.action == "destroy" and request.user.permission.filter(module__iexact="client",
                                                                       method="delete").count() >= 1:
            return True
        return False
