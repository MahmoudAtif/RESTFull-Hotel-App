from django.db import models

# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hotel(AbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class HotelImages(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='hotel_images')

    def __str__(self):
        return str(self.hotel)


class PhoneNumber(AbstractModel):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='numbers'
    )
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class HotelSocialMedia(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='social_media'
    )
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class WeekDays(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class OpeningHour(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='days'
    )
    name = models.OneToOneField(
        WeekDays,
        on_delete=models.CASCADE,
        related_name='days'
    )
    opens_at = models.TimeField()
    closes_at = models.TimeField()

    def __str__(self):
        return str(self.name)
