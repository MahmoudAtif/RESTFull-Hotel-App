from django.urls import path, include
from . import views
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('email-verification/', views.EmailVerificationView.as_view(),
         name='email-verification'),
    path('resend-activate/', views.ResendActivate.as_view(), name='resend-activate'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('confirm-reset-password/', views.ConfirmResetPasswordView.as_view(),
         name='confirm-reset-password'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    #     path('', include(router.urls)),    
    path('device-register/', views.DeviceRegisterView.as_view(), name='device-register'),
    path('device-disable/', views.DeviceDisableView.as_view(), name='device-disable'),
]
