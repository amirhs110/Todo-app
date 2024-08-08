from django.urls import path, include
from .views import (
    HomeView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskEditView,
    TaskDeleteView,
    TaskDoneView,
    TaskDetailEditView,
    TaskDetailDeleteView,
)

app_name = "task"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", TaskListView.as_view(), name="dashboard"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("task/create/", TaskCreateView.as_view(), name="create"),
    path("task/edit/<int:pk>/", TaskEditView.as_view(), name="edit"),
    path(
        "task/detail-edit/<int:pk>/", TaskDetailEditView.as_view(), name="detail-edit"
    ),
    path("task/delete/<int:pk>/", TaskDeleteView.as_view(), name="delete"),
    path(
        "task/detail-delete/<int:pk>/",
        TaskDetailDeleteView.as_view(),
        name="detail-delete",
    ),
    path("task/done/<int:pk>/", TaskDoneView.as_view(), name="done"),
    path("api/v1/", include("task.api.v1.urls")),
]
