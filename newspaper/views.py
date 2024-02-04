from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from newspaper.models import Newspaper, Topic, Redactor


@login_required
def index(request: HttpRequest) -> HttpResponse:
    topics_count = Topic.objects.count()
    newspapers_count = Newspaper.objects.count()
    redactors_count = Redactor.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "topics_count": topics_count,
        "newspapers_count": newspapers_count,
        "redactors_count": redactors_count,
        "num_visits": num_visits + 1
    }

    return render(
        request,
        "newspaper/index.html",
        context=context
    )
