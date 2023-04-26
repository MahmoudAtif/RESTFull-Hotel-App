from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce
from Hotel.models import AbstractModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Create your models here.


class Cart(AbstractModel):
    guest = models.OneToOneField(
        "Guest.Guest",
        verbose_name=_("Guest"),
        on_delete=models.CASCADE,
    )
    total = models.FloatField(default=0.0)
    sub_total = models.FloatField(default=0.0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id:
            self._recalculate_cart()

    def _calculate_sub_total(self):
        total = self.items.aggregate(
            sum=Coalesce(
                models.Sum(F('room__price') * F('days')),
                0,
                output_field=models.FloatField()
            ),

        )['sum']
        self.sub_total = total
        self.total = total
        return total

    def clear(self):
        self.items.all().delete()
        self.total = 0
        self.sub_total = 0
        self.save()
        return True

    def _recalculate_cart(self):
        self._calculate_sub_total()
        self.save()

    def __str__(self):
        return str(self.guest)


class CartItem(AbstractModel):
    cart = models.ForeignKey(
        Cart,
        verbose_name=_("Cart"),
        related_name='items',
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "Room.Room",
        verbose_name=_("Room"),
        related_name='items',
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    days = models.IntegerField(
        _("Days"),
        validators=[
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return f'{self.cart} - {self.room}'
