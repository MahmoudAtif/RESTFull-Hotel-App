from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reservations', views.ReservationViewSet, basename='reservations')

urlpatterns = [
    path('', include(router.urls)),
    # path('reservation/', views.ReservationView.as_view(), name='reservation'),
    # path('reservation-details/<int:id>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
]
