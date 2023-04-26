from django.db import models
from Hotel.models import AbstractModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
# Create your models here.


class Reservation(AbstractModel):

    class StatusEnum(models.IntegerChoices):
        PENDING = 1, 'Pending'
        COMPLETED = 2, 'Completed'
        CANCELED = 3, 'Canceled'

    guest = models.ForeignKey(
        'Guest.Guest',
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    status = models.IntegerField(
        choices=StatusEnum.choices,
        default=StatusEnum.PENDING
    )
    by_employee = models.ForeignKey(
        'Employee.Employee',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reserved_rooms'
    )
    total = models.FloatField(default=0.0)
    sub_total = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.guest)

    def check_reserved_rooms_count(self):
        count = self.reserved_rooms.all().count()
        if not count > 1:
            raise ValidationError(
                {
                    'error': 'reservation must be at least one reserved room'
                }
            )
        return True


class ReservedRoom(AbstractModel):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='reserved_rooms'
    )
    room = models.ForeignKey(
        'Room.Room',
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    guests = models.ManyToManyField("Guest.Guest", blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    days = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.FloatField(blank=True)

    def __str__(self):
        return f'{self.reservation} - {self.room}'


class CancelReservation(AbstractModel):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.reservation)
