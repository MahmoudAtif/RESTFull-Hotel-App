from django.contrib import admin
from . import models
from django import forms
# Register your models here.


class ReservedRoomInline(admin.StackedInline):
    model = models.ReservedRoom
    extra = 1


class CancelReservationInline(admin.StackedInline):
    model = models.CancelReservation



@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = (ReservedRoomInline, CancelReservationInline)

admin.site.register(models.ReservedRoom)
admin.site.register(models.CancelReservation)