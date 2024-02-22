from django.contrib.auth import get_user_model
from django.contrib import admin
from django.test import TestCase, Client
from django.urls import reverse

from newspaper.admin import RedactorAdmin, NewspaperAdmin
from newspaper.models import Redactor, Newspaper


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="Test_AdmiN",
            email="admin@gmail.com",
            password="AdminTest123321##",
        )
        self.client.force_login(self.admin_user)

    def test_redactor_admin_display(self):
        """
        Test that RedactorAdmin displays the required fields
        return None
        """
        redactor_admin = RedactorAdmin(Redactor, admin.site)
        self.assertEqual(redactor_admin.list_display, [
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        ]
        )

    def test_newspaper_admin(self):
        """
        Test that NewspaperAdmin has a search by title
        return None
        """
        newspaper_admin = NewspaperAdmin(Newspaper, admin.site)
        self.assertEqual(newspaper_admin.search_fields, ['title'])

    def test_topic_registered(self):
        """
        Test check that the Manufacturer is registered in the admin
        return None
        """
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "Topic")

    def test_redactor_add_page(self):
        """
        Test that the driver adding page is available
        return None
        """
        response = self.client.get(reverse("admin:newspaper_redactor_add"))
        self.assertEqual(response.status_code, 200)
