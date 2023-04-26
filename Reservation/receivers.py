from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Reservation, CancelReservation, ReservedRoom
from django.db import transaction


# @receiver(post_save, sender=Reservation)
# def create_reservation_invoice(sender, instance, created, **kwargs):
#     transaction.on_commit(lambda: instance.create_invoice())


# @receiver(post_save, sender=Reservation)
# def create_cancel_reservation(sender, instance, created, **kwargs):
#     if instance.status == 3:  # CANCELED
#         CancelReservation.objects.get_or_create(
#             reservation=instance,
#         )

@receiver(pre_save, sender=ReservedRoom)
def set_price_and_days_for_reserved_room(sender, instance, **kwargs):
    if not instance.price:
        instance.price = instance.room.price
    days = (instance.end_date - instance.start_date).days
    instance.days = int(days)
    return True
