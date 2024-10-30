from django.test import TestCase
from .models import User, Profile


class TestModels(TestCase):
    def test_user_model(self):
        u = User.objects.create(
            username="testuser", email="testuser@user.com", password="secret"
        )
        self.assertEqual(str(u), "testuser")

    def test_profile_model(self):
        """
        Tests that the Profile model is created when a User is created, as specified in signals.py.
        Also tests that the __str__ method returns the username of the User.
        """
        u = User.objects.create(
            username="testuser", email="testuser@user.com", password="secret"
        )
        p = u.profile
        self.assertEqual(str(p), "testuser")


