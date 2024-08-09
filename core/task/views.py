# from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task/dashboard.html"
    paginate_by = 6
    ordering = "-id"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "content"]
    success_url = reverse_lazy("task:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "content"]
    success_url = reverse_lazy("task:dashboard")


class TaskDetailEditView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "content"]
    success_url = reverse_lazy("task:dashboard")

    template_name = "task/update_task.html"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task:dashboard")


class TaskDetailDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task:dashboard")


class TaskDoneView(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("task:dashboard")

    def get(self, request, *args, **kwargs):
        obj = Task.objects.get(id=kwargs.get("pk"))
        if obj.complete:
            obj.complete = False
        else:
            obj.complete = True
        obj.save()
        return redirect(self.success_url)
