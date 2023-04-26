from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class RoomType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.IntegerField()
    room_type = models.ForeignKey(
        RoomType,
        verbose_name=('Type'),
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    description = models.TextField(null=True, blank=True)
    discount = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    price = models.FloatField()
    is_available = models.BooleanField(verbose_name='Available', default=True)
    smoke = models.BooleanField(verbose_name='Can Smoke', default=False)

    def __str__(self):
        return str(self.number)

    def get_price_after_discount(self):
        total = self.price - (self.price * self.discount/100.0)
        return total
