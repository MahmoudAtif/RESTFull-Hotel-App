from User.models import User
from rest_framework.test import APITestCase


class TestModel(APITestCase):
    
    def test_create_user_manager(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='test'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser_manager(self):
        user = User.objects.create_superuser(
            username='testsuperuser',
            email='testsuperuser@gmail.com',
            password='test'
        )
        self.assertEqual(user.username, 'testsuperuser')
        self.assertEqual(user.email, 'testsuperuser@gmail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)



