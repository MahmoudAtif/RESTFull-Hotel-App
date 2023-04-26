from django.db.models.signals import post_save
from django.dispatch import receiver
from User.models import User
from .tasks import send_email_verification


@receiver(post_save, sender=User)
def send_email_activation(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        url_name = 'email-verification'
        send_email_verification.delay(
            subject='Email Activation',
            email=instance.email,
            url_name=url_name,
        )
