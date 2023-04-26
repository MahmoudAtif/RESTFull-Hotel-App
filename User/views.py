from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from User.models import User
from rest_framework_simplejwt.views import TokenBlacklistView
from . import messages

# Create your views here.


class SignUpView(APIView):

    permission_classes = ()
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Check your Email for Verification'
                },
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):

    permission_classes = ()
    serializer_class = serializers.SignInSerializer
    throttle_scope = 'login'

    def send_user_notification(self, user):
        user.send_notification(
            title='Login',
            body='There was a login to your account'
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # self.send_user_notification(user=serializer.validated_data['user'])
            return Response(
                {
                    'access_token': serializer.validated_data['access_token'],
                    'refresh_token': serializer.validated_data['refresh_token'],
                },
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):

    permission_classes = ()

    def get_object(self):
        uuid = self.request.GET.get('uuid')
        user = User.get_object_uuid(uuid=uuid)
        return user

    def check_token(self, user):
        token = self.request.GET.get('token')
        return user.check_token_validation(token)

    def get(self, request):
        user = self.get_object()

        if not user:
            return Response(
                {'message': 'user not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_token(user)

        if user.is_active:
            return Response(
                {'message': 'user is already activated'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.activate()
        user.send_success_email(
            subject=messages.SUCCESS_ACTIVATION_SUBJECT,
            message=messages.SUCCESS_ACTIVATION_MESSAGE
        )
        return Response(
            {'messsage': 'Success verification, you are active now'},
            status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):

    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid():
            if user.check_password(serializer.validated_data['old_password']):
                user.change_password(serializer.validated_data['new_password'])
                user.send_success_email(
                    subject=messages.SUCCESS_CHANGE_PASSWORD_SUBJECT,
                    message=messages.SUCCESS_CHANGE_PASSWORD_MESSAGE
                )
                return Response({'Your password changed successfully'}, status=status.HTTP_200_OK)
            return Response({'old_password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):

    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = ()
    throttle_scope = 'reset_password'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.send_reset_password_email()

            return Response(
                {'Check your email for reset password'},
                status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetPasswordView(APIView):

    serializer_class = serializers.ConfirmResetPasswordSerializer
    permission_classes = ()

    def get_object(self):
        uuid = self.request.GET.get('uuid')
        user = User.get_object_uuid(uuid=uuid)
        return user

    def check_token(self, user):
        token = self.request.GET.get('token')
        return user.check_token_validation(token)

    def reset_password(self, user):
        new_password = self.request.data['new_password']
        return user.change_password(password=new_password)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = self.get_object()

            if not user:
                return Response(
                    {'message': 'user not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            self.check_token(user)
            user.send_success_email(
                subject=messages.SUCCESS_RESET_PASSWORD_SUBJECT,
                message=messages.SUCCESS_RESET_PASSWORD_MESSAGE
            )
            return Response({'Password reset successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(TokenBlacklistView):

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(
            data={
                'message': 'The refresh token is blacklisted'
            }
        )


class ResendActivate(APIView):

    serializer_classes = serializers.ResendActivateSerializer
    permission_classes = ()
    throttle_scope = 'resend_activate'

    def post(self, request):
        serializer = self.serializer_classes(data=request.data)
        if serializer.is_valid():
            return Response(
                {'message': 'Check your email for activation'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationView(APIView):

    def get(self, request):
        FCMDevice.objects.get(id=1).send_message(
            Message(
                notification=Notification(
                    title="title",
                    body="body",
                    image="image_url"
                )
            )
        )
        return Response({'ok': 'ok'})


class DeviceRegisterView(APIView):

    serializer_classes = serializers.DeviceRegisterSerializer

    def post(self, request):
        serializer = self.serializer_classes(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceDisableView(APIView):

    serializer_classes = serializers.DeviceDisableSerializer

    def device_disable(self, device):
        device.active = False
        device.save()

    def post(self, request):
        serializer = self.serializer_classes(data=request.data)

        if serializer.is_valid():
            device = serializer.validated_data['device']
            self.device_disable(device)
            return Response(
                {'message': 'Device disabled'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
