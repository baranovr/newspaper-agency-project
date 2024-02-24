from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from newspaper_agency_project import settings

from datetime import date


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_absolute_url(self):
        return reverse(
            "newspaper:redactor-detail", kwargs={"pk": self.pk}
        )


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(default=date.today)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="newspaper"
    )

    def __str__(self):
        return f"{self.title}"
