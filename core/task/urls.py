from django.urls import path
from .views import HomeView, TaskListView, TaskDetailView, TaskCreateView

app_name = 'task'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('dashboard/', TaskListView.as_view(), name="dashboard"),
    path('task/<int:pk>/', TaskDetailView.as_view(), name="detail"),
    path('task/create/', TaskCreateView.as_view(), name="task-create"),
]