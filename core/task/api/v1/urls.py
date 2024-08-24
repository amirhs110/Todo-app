from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSets,get_weather_data

app_name = "api-v1"


router = DefaultRouter()
router.register("", TaskViewSets, basename="task")

urlpatterns = [
    path('weather-data/', get_weather_data , name='weather-data')
]


urlpatterns += router.urls
