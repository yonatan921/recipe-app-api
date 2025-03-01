"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """

    """

    def test_creat_user_with_email_successful(self):
        """

        :return:
        """
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """

        :return:
        """
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"]
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sampl123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """

        :return:
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', "test123")

    def test_create_superuser(self):
        """

        :return:
        """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            "test123",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
