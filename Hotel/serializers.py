from rest_framework import serializers
from . import models


class HotelImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelImages
        fields = ('image',)


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhoneNumber
        fields = ('number',)


class HotelSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelSocialMedia
        fields = ('name', 'url', 'icon',)


class OpeningHourMediaSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()

    class Meta:
        model = models.OpeningHour
        fields = ('name', 'opens_at', 'closes_at',)


class HotelSerializer(serializers.ModelSerializer):
    images = HotelImagesSerializer(read_only=True, many=True)
    numbers = PhoneNumberSerializer(read_only=True, many=True)
    social_media = HotelSocialMediaSerializer(read_only=True, many=True)
    days = OpeningHourMediaSerializer(read_only=True, many=True)

    class Meta:
        model = models.Hotel
        fields = '__all__'
