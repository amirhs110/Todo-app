# from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSets

app_name = "api-v1"


router = DefaultRouter()
router.register("", TaskViewSets , basename="task")

urlpatterns = []


urlpatterns += router.urls
