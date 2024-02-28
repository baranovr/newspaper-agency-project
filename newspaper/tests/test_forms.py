from django.test import TestCase
from django.utils.timezone import now

from newspaper.forms import RedactorCreationForm


class FormsTests(TestCase):
    def test_redactor_creation_form_with_custom_fields(self):
        form_fields_data = {
            "username": "Test_User1name",
            "first_name": "First",
            "last_name": "Last",
            "email": "test@gmail.com",
            "years_of_experience": 2,
            "password1": "Test123321##",
            "password2": "Test123321##",
            "date_joined": now(),
        }
        form = RedactorCreationForm(data=form_fields_data)

        if not form.is_valid():
            print(f"Error in validation: {form.errors}")

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_fields_data)
