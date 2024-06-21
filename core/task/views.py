from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Task

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

class TaskListView(ListView):
    template_name = 'task/dashboard.html'
    queryset= Task.objects.all()
    paginate_by = 6
    ordering = "-id"