from rest_framework import serializers
from .models import Cart, CartItem
from Room.models import Room
from django.core.validators import MinValueValidator


class CartItemSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        exclude = ['cart']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        exclude = ['guest']


class AddToCartSerializer(serializers.Serializer):
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.filter(is_available=True)
    )
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()


class UpdateCartSerilaizer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
