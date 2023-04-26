from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CartItem


@receiver(pre_save, sender=CartItem)
def set_days_for_cart_item(sender, instance, **kwargs):
    days = (instance.end_date - instance.start_date).days
    instance.days = int(days)
    return True
