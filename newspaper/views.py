from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newspaper.forms import RedactorCreationForm, TopicSearchForm, \
    NewspaperSearchForm, RedactorSearchForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.all()
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspaper__topic")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "years_of_experience",
        "date_joined"
    ]
    success_url = reverse_lazy("newspaper:redactor-list")
    template_name = "newspaper/redactor_form.html"


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    fields = "__all__"
    success_url = reverse_lazy("newspaper:redactor-list")
    template_name = "newspaper/redactor_confirm_delete.html"
