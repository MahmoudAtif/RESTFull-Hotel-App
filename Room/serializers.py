from rest_framework import serializers
from . import models


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    room_type = serializers.StringRelatedField()

    class Meta:
        model = models.Room
        fields = ('url', 'id', 'number', 'description', 'room_type', 'price')


class RoomDetailSerilaizer(serializers.ModelSerializer):
    room_type = serializers.StringRelatedField()
    floor = serializers.StringRelatedField()

    class Meta:
        model = models.Room
        fields = '__all__'
