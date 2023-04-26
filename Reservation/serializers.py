from rest_framework import serializers
from . import models


class ReservedRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReservedRoom
        exclude = ['reservation']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = [
            'id',
            'total',
            'sub_total',
            'status',
            'created_at',
            'updated_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = models.Reservation.StatusEnum(
            instance.status
        ).label
        return representation


class ReservationDetailSerializer(serializers.ModelSerializer):
    reserved_rooms = ReservedRoomSerializer(read_only=True, many=True)

    class Meta:
        model = models.Reservation
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = models.Reservation.StatusEnum(
            instance.status
        ).label
        return representation
