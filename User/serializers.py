from rest_framework import serializers
from User.models import User
from .backends import CustomBackends
from .token import GenerateToken
from django.db import transaction
from fcm_django.models import FCMDevice


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm',)
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs['password_confirm']

        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError({
                "error": "password didn't match !!"
            })

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.disable()
        return user


class SignInSerializer(serializers.Serializer):
    email_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_username = attrs['email_username']
        password = attrs['password']

        user = CustomBackends.authenticate(
            username=email_username, password=password)

        if user is not None:
            if not user.is_active:
                raise serializers.ValidationError({
                    'error': 'Your account is disabled',
                })
        else:
            raise serializers.ValidationError({
                'error': 'unable to login with provided credential'
            })

        attrs['user'] = user
        token = GenerateToken.get_token(user)

        attrs['access_token'] = token['access_token']
        attrs['refresh_token'] = token['refresh_token']
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs['email']
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError({
                'error': 'email address does not exist '
            })

        attrs['user'] = user
        return super().validate(attrs)


class ConfirmResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    new_password_confirmation = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs['new_password']
        new_password_confirmation = attrs['new_password_confirmation']

        if new_password and new_password_confirmation and new_password != new_password_confirmation:
            raise serializers.ValidationError({
                "error": "password didn't match!!"
            })
        return super().validate(attrs)


class ResendActivateSerializer(serializers.Serializer):
    email_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_username = attrs['email_username']
        password = attrs['password']

        user = CustomBackends.authenticate(
            username=email_username,
            password=password
        )

        if user is not None:
            if not user.is_active:
                user.send_email_activation()
            else:
                raise serializers.ValidationError({
                    'message': 'User with provided crediential is already activated'
                })
        else:
            raise serializers.ValidationError({
                'message': 'unable to login with provided credential'
            })

        return attrs


class DeviceRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMDevice
        fields = ('user', 'registration_id', )

    def create(self, validated_data):
        device, created = FCMDevice.objects.get_or_create(**validated_data)

        if device:
            device.active = True
            device.save()
        return device


class DeviceDisableSerializer(serializers.Serializer):
    registration_token = serializers.CharField()

    def validate(self, attrs):
        registration_token = attrs.get('registration_token')
        device = FCMDevice.objects.filter(
            registration_id=registration_token
        ).first()

        if not device:
            raise serializers.ValidationError(
                {
                    'message': 'this device is not exist'
                }
            )
        attrs['device'] = device
        return attrs
