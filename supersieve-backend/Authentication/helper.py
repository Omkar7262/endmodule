from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from plivo import RestClient
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.exceptions import APIException, _get_error_details as error_details
from rest_framework.status import *
from django.utils.translation import gettext_lazy as _
from .models import UserRole, PermissionPattern
from django.db.models import Q
from supersieve.constant import USER_TYPE


class MobileException(APIException):
    status_code = HTTP_417_EXPECTATION_FAILED
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = error_details(detail, code)


def send_otp_twilio(otp, mobile):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=f'PuffNRoll, Your one time password is {otp}',
                                         from_=settings.TWILIO_PHONE_NO,
                                         to=mobile)
        return message.sid
    except TwilioException as e:
        print(e)
        raise MobileException({"mobile": e})


def send_otp_by_plivo(otp, mobile):
    client = RestClient(settings.PLIVO_ACCOUNT_SID, settings.PLIVO_AUTH_TOKEN)
    message_created = client.messages.create(
        src='72728436367',
        dst=mobile,
        text=f'PuffNRoll -> Your one time password is {otp}',
    )
    return message_created.api_id


def call_for_otp_by_twilio(otp, mobile):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = 'media/response.xml'
    with open(response, 'w+') as file:
        var = file.read()
        file.write(
            f'<?xml version="1.0" encoding="UTF-8"?><Response><Say loop="2">Hello,This is PuffNRoll. Your Login One Time Password Is:-  <prosody rate="70%"><say-as interpret-as="telephone"> {otp}</say-as></prosody></Say></Response>')
    call = client.calls.create(
        to=mobile,
        from_=settings.TWILIO_PHONE_NO,
        url=settings.URL + response
    )
    return call.status


def send_email_otp(name, otp, email):
    message = {
        'user': name,
        'site_name': "PuffNRoll",
        'otp': otp,
    }
    mail_subject = "Verify you PuffNRoll Account"
    plain_text = get_template('Email/EmailVerification/email_one_time_password_template.txt').render(message)
    htmly = get_template('Email/EmailVerification/email_one_time_password_template.html').render(message)

    msg = EmailMultiAlternatives(mail_subject, plain_text, settings.EMAIL_HOST_USER,
                                 [email])
    msg.attach_alternative(htmly, "text/html")
    msg.send()


def send_email(context, subject, tosend, html_template, txt_template):
    # Hello World
    mail_subject = subject
    plain_text = get_template(txt_template).render(context)
    htmly = get_template(html_template).render(context)

    msg = EmailMultiAlternatives(mail_subject, plain_text, settings.EMAIL_HOST_USER,
                                 [tosend])
    msg.attach_alternative(htmly, "text/html")
    msg.send()


def update_permission(user):
    user_type = USER_TYPE[user.user_type]
    user_role = UserRole.objects.filter(rn=user_type)
    a = PermissionPattern.objects.filter(user_type__contains=user.user_type)
    values = a.values_list('id', flat=True)
    print(values)
    q_object = Q()
    for i in values:
        q_object &= Q(id=i)
    if not user_role:
        user_role = UserRole.objects.create(rn=user_type)
        user_role.up.add(*values)
        user_role.save()
        user.user_role = user_role
    else:
        user.user_role = user_role[0]
    user.save()


def send_otp(otp, mobile):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(body=f'Twilio -> Your one time password is {otp}',
                                     from_=settings.TWILIO_PHONE_NO,
                                     to=mobile, messaging_service_sid=settings.MSG_SERVICE_ID)
    return message.sid


