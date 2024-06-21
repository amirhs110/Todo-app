from django.urls import path
from .views import HomeView, TaskListView

app_name = 'task'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('dashboard/', TaskListView.as_view(), name="dashboard")
]