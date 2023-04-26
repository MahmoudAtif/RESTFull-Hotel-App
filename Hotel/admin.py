from django.contrib import admin
from . import models
# Register your models here.


class OpeningHourInlines(admin.TabularInline):
    model = models.OpeningHour
    extra = 1


class PhoneNumberInline(admin.TabularInline):
    model = models.PhoneNumber
    extra = 1


class ImagesInline(admin.TabularInline):
    model = models.HotelImages
    extra = 1


class SocialMediaInline(admin.TabularInline):
    model = models.HotelSocialMedia
    extra = 1


@admin.register(models.Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = (
        OpeningHourInlines,
        PhoneNumberInline,
        ImagesInline,
        SocialMediaInline
    )


admin.site.register(models.WeekDays)
admin.site.register(models.OpeningHour)
admin.site.register(models.PhoneNumber)
