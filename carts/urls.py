from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('my-cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls))
]
