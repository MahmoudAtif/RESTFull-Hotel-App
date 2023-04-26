from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from User.managers import UserManager
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError
from .tasks import (
    send_email_verification,
    send_success_email,
    send_notification_task,
)
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self) -> str:
        return super().get_full_name()

    def activate(self):
        self.is_active = True
        self.save()

    def disable(self):
        self.is_active = False
        self.save()

    def get_user_uuid(self):
        """ generate uuid for user """
        uuid = urlsafe_base64_encode(force_bytes(self.id))
        return uuid

    @classmethod
    def get_object_uuid(cls, uuid):
        """ get user object from  uuid """
        try:
            uid = urlsafe_base64_decode(uuid).decode()
            user = cls.objects.filter(id=uid).first()
        except:
            return None
        return user

    def generate_token(self):
        """ 
        generate token for user to reset password or
        email activation
        """
        token = default_token_generator.make_token(self)
        return token

    def check_token_validation(self, token):
        """ return true if token is not expired """
        if not default_token_generator.check_token(self, token):
            raise ValidationError({'message': 'Token is invalid or expired'})
        return True

    def change_password(self, password):
        self.set_password(password)
        self.save()

    def send_email_activation(self):
        if not self.is_active:
            url_name = 'email-verification'
            send_email_verification.delay(
                subject='Email Activation',
                email=self.email,
                url_name=url_name,
            )
        return True

    def send_reset_password_email(self):
        url_name = 'confirm-reset-password'
        send_email_verification.delay(
            subject='Reset Password',
            email=self.email,
            url_name=url_name,
        )
        return True

    def send_success_email(self, subject, message):
        send_success_email.delay(
            subject=subject,
            message=message,
            email=self.email
        )
        return True

    def send_notification(self, title, body):
        send_notification_task.delay(
            user=self.id,
            title=title,
            body=body,
        )
        return True
