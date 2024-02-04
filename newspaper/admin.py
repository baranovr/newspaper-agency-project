from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from newspaper.models import Redactor, Newspaper, Topic


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "years_of_experience"
    ]
    search_fields = ["username", "first_name", "last_name"]
    ordering = ["username", ]
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ["years_of_experience"]}),
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ["title", "published_date", "topic"]
    search_fields = ["title"]
    list_filter = ["published_date"]
    ordering = ["title", ]


admin.site.register(Topic)
