from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

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


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "newspaper/topic_list.html"
    paginate_by = 5


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")
    template_name = "newspaper/topic_form.html"


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")
    template_name = "newspaper/topic_form.html"


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper:topic-list")
    template_name = "newspaper/topic_confirm_delete.html"


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.all().select_related("topic")
    paginate_by = 5


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("newspaper:newspaper-list")
    template_name = "newspaper/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("newspaper:newspaper-list")
    template_name = "newspaper/newspaper_form.html"


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("newspaper:newspaper-list")
    template_name = "newspaper/newspaper_confirm_delete.html"


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5
