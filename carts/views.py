from django.db import transaction
from rest_framework.exceptions import NotFound
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer, UpdateCartSerilaizer
from rest_framework.decorators import action
from Reservation.models import Reservation, ReservedRoom
from Reservation.serializers import ReservationSerializer

# Create your views here.


class CartViewSet(viewsets.GenericViewSet):

    serializer_class = CartSerializer

    def get_object(self):
        guest = self.request.user.guest
        cart, created = Cart.objects.get_or_create(guest=guest)
        return cart

    def list(self, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart, many=False)
        return Response(
            {
                'messgae': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False
    )
    def add(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data['room']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        # add item to cart
        CartItem.objects.create(
            cart=cart,
            room=room,
            start_date=start_date,
            end_date=end_date,
        )
        return Response(
            {
                'messgae': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path=r'items/(?P<pk>[^/.]+)/remove'
    )
    def remove(self, *args, **kwargs):
        cart = self.get_object()
        pk = kwargs.get('pk')
        cart_item = cart.items.filter(pk=pk).first()
        self.check_item(cart_item)
        cart_item.delete()
        return Response(
            {
                'messgae': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path=r'items/(?P<pk>[^/.]+)/update-date'
    )
    def update_date(self, request, *args, **kwargs):
        serializer = UpdateCartSerilaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self.get_object()

        pk = kwargs.get('pk')
        cart_item = cart.items.filter(pk=pk).first()
        self.check_item(cart_item)

        # update room date
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        cart_item.end_date = start_date
        cart_item.end_date = end_date
        cart_item.save()
        return Response(
            {
                'message': 'SUCCESS'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['Post'],
        detail=False
    )
    def clear(self, *args, **kwargs):
        cart = self.get_object()
        cart.clear()
        return Response(
            {
                'messgae': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        methods=['POST'],
        detail=False
    )
    def checkout_reservation(self, request, *args, **kwargs):
        cart = self.get_object()
        cart_items = cart.items.select_related('room')
        if not cart_items:
            return Response(
                {
                    'error': 'Cart is empty',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation = Reservation.objects.create(
            guest=request.user.guest,
            sub_total=cart.sub_total,
            total=cart.total,
        )

        for item in cart_items:
            room = ReservedRoom.objects.create(
                reservation=reservation,
                room=item.room,
                start_date=item.start_date,
                end_date=item.end_date,
                price=item.room.price
            )
            room.guests.add(self.request.user.guest)
            room.save()
        cart.clear()
        serializer = ReservationSerializer(reservation, many=False)
        return Response(
            {
                'message': 'SUCCESS',
                'data': serializer.data
            }
        )

    def check_item(self, cart_item):
        if not cart_item:
            raise NotFound(
                {
                    'error': 'Not Found',
                },
            )
        return True
