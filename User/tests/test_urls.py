from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from User import views


class TestUrl(APITestCase):

    def test_sign_up_url(self):
        url = reverse('sign-up')
        view = resolve(url).func.view_class
        self.assertEqual(view, views.SignUpView)

    def test_sign_in_url(self):
        url = reverse('sign-in')
        view = resolve(url).func.view_class
        self.assertEqual(view, views.SignInView)

    def test_email_verification_url(self):
        url = reverse('email-verification')
        view = resolve(url).func.view_class
        self.assertEqual(view, views.EmailVerificationView)
    
    def test_change_password_url(self):
        url = reverse('change-password')
        view = resolve(url).func.view_class
        self.assertEqual(view, views.ChangePasswordView)
    
    def test_reset_password_url(self):
        url = reverse('reset-password')
        view = resolve(url).func.view_class
        self.assertEqual(view, views.ResetPasswordView)
    
    def test_confirm_reset_password_url(self):
        url = reverse('confirm-reset-password')
        view = resolve(url).func.view_class
        self.assertEqual(view, views.ConfirmResetPasswordView)

    def test_logout_url(self):
        url = reverse('logout')
        view =resolve(url).func.view_class
        self.assertEqual(view, views.LogoutView)