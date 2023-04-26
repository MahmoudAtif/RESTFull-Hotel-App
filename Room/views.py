from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from . import serializers
from . import models
# Create your views here.


class RoomView(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = models.Room.objects.select_related('room_type')
    filter_backends = [SearchFilter]
    search_fields = ['description', 'room_type__name']
    serializer_class = serializers.RoomSerializer
    authentication_classes = ()
    permission_classes = ()

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().filter(pk=pk).first()

        if not instance:
            return Response(
                {
                    'error': 'Not Found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.RoomDetailSerilaizer(instance)
        return Response(
            {
                'messgse': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )