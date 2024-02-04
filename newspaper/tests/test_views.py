from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.models import Redactor

REDACTOR_URL = reverse("newspaper:redactor-list")


class PublicRedactorTest(TestCase):
    def test_login_required(self):
        response = self.client.get(REDACTOR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateRedactorTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin1",
            password="Test123321#",
            years_of_experience=2
        )
        self.client.force_login(self.user)

    def test_retrieve_redactors(self):
        Redactor.objects.create(
            username="AdMin",
            password="TesT123321#",
            years_of_experience=3
        )
        Redactor.objects.create(
            username="ADMIn",
            password="TEsT123321#",
            years_of_experience=4
        )
        response = self.client.get(REDACTOR_URL)
        self.assertEqual(response.status_code, 200)

        redactors = Redactor.objects.all()
        self.assertEqual(
            list(response.context["redactor_list"]), list(redactors)
        )
        self.assertTemplateUsed(
            response, "newspaper/redactor_list.html"
        )
