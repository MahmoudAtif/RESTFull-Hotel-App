from . import serializers
from . import models
from rest_framework.generics import ListAPIView
# Create your views here.


class HotelView(ListAPIView):
    queryset = models.Hotel.objects.prefetch_related(
        'images',
        'numbers',
        'social_media',
        'days'
    )
    serializer_class = serializers.HotelSerializer
    authentication_classes = ()
    permission_classes = ()
