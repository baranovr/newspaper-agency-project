from django.contrib.auth import get_user_model
from django.test import TestCase

from newspaper.models import Newspaper, Topic

from datetime import date


class ModelTest(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(
            name="Topicname",
        )
        expected_result = f"{topic.name}"
        self.assertEqual(str(topic), expected_result)

    def test_create_redactor_and_str(self):
        first_name = "First"
        last_name = "Last"
        username = "UseR_NamE1"
        password = "Test123321##"
        years_of_experience = 2

        redactor = get_user_model().objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEqual(redactor.first_name, first_name)
        self.assertEqual(redactor.last_name, last_name)
        self.assertEqual(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEqual(redactor.years_of_experience, years_of_experience)

        expected_result = (
            f"{redactor.first_name} {redactor.last_name} ({redactor.username})"
        )
        self.assertEqual(str(redactor), expected_result)

    def test_create_newspaper_and_str(self):
        title = "Title"
        content = "Some content for testing"
        published_date = date.today()
        topic = Topic.objects.create(name="Test Topic")

        newspaper = Newspaper.objects.create(
            title=title,
            content=content,
            published_date=published_date,
            topic=topic,
        )

        self.assertEqual(newspaper.title, title)
        self.assertEqual(newspaper.content, content)
        self.assertEqual(newspaper.published_date, published_date)
        self.assertEqual(newspaper.topic, topic)

        expected_result = f"{newspaper.title}"
        self.assertEqual(str(newspaper), expected_result)
