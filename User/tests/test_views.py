from rest_framework.test import APITestCase
from django.urls import reverse
from User import views
from rest_framework import status
from User.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


class TestView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@gmail.com',
            password='test'
        )

        self.unactive_user = User.objects.create_user(
            username='unactive',
            email='unactive@gmail.com',
            password='unactive',
            is_active=False
        )

    def test_sign_up_get(self):
        url = reverse('sign-up')
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_sign_up_post(self):
        url = reverse('sign-up')
        data = {
            'username': 'test1',
            'email': 'test1@gmail.com',
            'password': 'test123456789',
            'password_confirm': 'test123456789'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['username'], 'test1')
        self.assertEqual(response.data['data']['email'], 'test1@gmail.com')

    def test_sign_up_put(self):
        url = reverse('sign-up')
        response = self.client.put(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_sign_up_delete(self):
        url = reverse('sign-up')
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_sign_in_get(self):
        url = reverse('sign-in')
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_email_sign_in_post(self):
        url = reverse('sign-in')
        data = {
            'email_username': 'test@gmail.com',
            'password': 'test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_username_sign_in_post(self):
        url = reverse('sign-in')
        data = {
            'email_username': 'test',
            'password': 'test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_in_post_without_data(self):
        url = reverse('sign-in')
        response = self.client.post(url)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_username_sign_in_post_unactive_user(self):
        url = reverse('sign-in')
        data = {
            'email_username': 'unactive',
            'password': 'unactive'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_email_verification_get(self):
        uuid = self.unactive_user.get_user_uuid()
        token = self.unactive_user.generate_token()
        url = f"{reverse('email-verification')}?token={token}&uuid={uuid}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_verification_get_with_wrong_uuid(self):
        token = self.unactive_user.generate_token()
        url = f"{reverse('email-verification')}?token={token}&uuid=MM"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'user not found')

    def test_email_verification_get_with_wrong_token(self):
        uuid = self.unactive_user.get_user_uuid()
        url = f"{reverse('email-verification')}?token=dsfsdgdfgdfghdfhdfgh&uuid={uuid}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         'Token is invalid or expired')

    def get_access_token(self):
        url = reverse('sign-in')
        data = {
            'email_username': 'test',
            'password': 'test'
        }
        response = self.client.post(url, data)
        return response.data['access_token']

    def get_refresh_token(self):
        url = reverse('sign-in')
        data = {
            'email_username': 'test',
            'password': 'test'
        }
        response = self.client.post(url, data)

        return response.data['refresh_token']

    def authorize_user(self):
        token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_change_password_get(self):
        url = reverse('change-password')
        self.authorize_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_change_password_post(self):
        url = reverse('change-password')
        self.authorize_user()
        data = {
            'old_password': 'test',
            'new_password': 'newtest'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_change_password_post_with_wrong_old_password(self):
        url = reverse('change-password')
        self.authorize_user()
        data = {
            'old_password': 'testddc',
            'new_password': 'newtest'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_change_password_post_without_data(self):
        url = reverse('change-password')
        self.authorize_user()
        response = self.client.post(url)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_reset_password_get(self):
        url = reverse('reset-password')
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_reset_password_post(self):
        url = reverse('reset-password')
        data = {
            'email': 'test@gmail.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_reset_password_post_with_wrong_email(self):
        url = reverse('reset-password')
        data = {
            'email': 'testWrong@gmail.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_reset_password_post_without_data(self):
        url = reverse('reset-password')
        response = self.client.post(url)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_confirm_reset_password_post(self):
        uuid = self.user.get_user_uuid()
        token = self.user.generate_token()
        url = f"{reverse('confirm-reset-password')}?token={token}&uuid={uuid}"
        data = {
            'new_password': 'test1232',
            'new_password_confirmation': 'test1232'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_logout_get(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_logout_post(self):
        url = reverse('logout')
        self.authorize_user()
        data = {
            'refresh': self.get_refresh_token()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'The refresh token is blacklisted')

    def test_logout_post_without_data(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_post_with_wrong_data(self):
        url = reverse('logout')
        self.authorize_user()
        data = {
            'refresh': 'fsgfdgd87g78fdgdfg8893wrweuf8'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
