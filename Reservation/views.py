from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from .serializers import ReservationSerializer, ReservationDetailSerializer
from .models import Reservation
from rest_framework.decorators import action
# Create your views here.


class ReservationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(guest=self.request.user.guest)
        return queryset

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = ReservationDetailSerializer(instance, many=False)
        return Response(
            {
                'message': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        url_path=r'reserved-rooms/(?P<reserved_room_pk>[^/.]+)/remove'
    )
    def remove_room(self, *args, **kwargs):
        instance = self.get_object()
        pk = kwargs.get('reserved_room_pk')
        reserved_room = instance.reserved_rooms.filter(pk=pk).first()
        if not reserved_room:
            return Response(
                {
                    'message': 'Not Found',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance.check_reserved_rooms_count()
        reserved_room.delete()
        return Response(
            {
                'message': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def cancel(self, *args, **kwargs):
        instance = self.get_object()
        instance.status = Reservation.StatusEnum.CANCELED
        instance.save()
        return Response(
            {
                'message': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def delete(self, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {
                'message': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )
