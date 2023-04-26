from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
from django.core.management import call_command
from User import models
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def activation_url(url_name, uuid, token):
    site = Site.objects.get_current()
    domain = site.domain
    relative_url = f"{reverse(url_name)}?token={token}&uuid={uuid}"
    activation_url = f'http://{domain}{relative_url}'
    return activation_url


@shared_task
def delete_inactivated_users():
    call_command(
        command_name='deleteinactiveusers'
    )
    return 'Done'


@shared_task
def send_email_verification(subject, email, url_name):
    user = models.User.objects.filter(email=email).first()
    token = user.generate_token()
    uuid = user.get_user_uuid()
    url = activation_url(url_name, uuid, token)
    message = f'Click Here for {subject} {url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'


@shared_task
def send_success_email(subject, message, email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'


@shared_task
def send_notification_task(user, title, body):
    device = FCMDevice.objects.filter(user=user, active=True)
    device.send_message(
        Message(
            notification=Notification(
                title=title,
                body=body,
            )
        )
    )
    return 'Done'
