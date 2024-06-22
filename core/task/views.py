from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import Task

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

class TaskListView(ListView):
    model = Task
    template_name = 'task/dashboard.html'
    paginate_by = 6
    ordering = "-id"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskDetailView(DetailView):
    model= Task

class TaskCreateView(CreateView):
    model = Task
    fields=['title', 'content']
    success_url = reverse_lazy("task:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)