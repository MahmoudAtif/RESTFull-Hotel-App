from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Guest(models.Model):
    user = models.OneToOneField(
        "User.User",
        verbose_name=_("User"),
        related_name='guest',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
