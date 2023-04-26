from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('hotel/', views.HotelView.as_view(), name='hotel')
]
