from django.urls import path
from .views import HomeView

app_name = 'task'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]