from rest_framework.viewsets import ModelViewSet

# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from django.shortcuts import get_object_or_404
from task.models import Task
from .serializers import TaskSerializer
from .paginations import TaskPagination
from .permissions import IsVerifiedUser
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class TaskViewSets(ModelViewSet):
    queryset = Task.objects.all().order_by("-created_date")
    serializer_class = TaskSerializer
    permission_classes = [IsVerifiedUser]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["complete"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            """
            when i run app and request to show swagger doc i see a type error:
            TypeError: Field 'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x7f9351027a90>.
            view's TaskViewSets raised exception during schema generation; use getattr(self, 'swagger_fake_view', False) to detect and short-circuit this

            The Type error is because drf_yasg is trying to generate the schema for your view and
            it's running into issues when it encounters *AnonymousUser objects*.
            The error message suggests that getattr(self, 'swagger_fake_view', False) can be used to detect and
            short-circuit this during schema generation.
            """
            # Return an empty queryset when generating schema
            return Task.objects.none()

        user = self.request.user
        tasks = Task.objects.filter(user=user).order_by("-created_date")
        return tasks

    @action(methods=["get"], detail=True)
    def get_done(self, request, pk=None):
        if getattr(self, "swagger_fake_view", False):
            # Return a placeholder response when generating schema
            return Response({"Status": "Done", "detail": {}})

        task = get_object_or_404(Task, pk=pk, user=request.user)
        if not task.complete:
            task.complete = True
            task.save()
            status = "Done"
        else:
            status = "Your task is already done."
        serializer = TaskSerializer(instance=task, context={"request": request})
        return Response(
            {
                "status": status,
                "detail": serializer.data,
            }
        )


@api_view(['get'])
def get_weather_data(request):
    # required data
    city = "Tehran"
    api_key = "d362f41af4f139e1fc31e4c1688f7b16"
    # get city data by Direct geocoding api
    api_get_city = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    city_data = requests.get(api_get_city).json()
    lat = city_data[0]['lat']
    lon = city_data[0]['lon']
    # get weather data
    api_weather = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=fa"
    weather_data = requests.get(api_weather).json()

    if weather_data.get("cod") != 200:
        return Response({"error": "Failed to retrieve weather data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Customize the response data
    customized_response = {
        'location': {
            'city': city_data[0]['name'],
            'country': city_data[0]['country']
        },
        'weather': {
            'temperature': weather_data['main']['temp'],  # Temperature in Celsius
            'min-temperature': weather_data['main']['temp_min'],  # Min temperature in Celsius
            'max-temperature': weather_data['main']['temp_max'],  # Max temperature in Celsius
            'description': weather_data['weather'][0]['description'],  # Weather description
            'wind_speed': weather_data['wind']['speed'],  # Wind speed in meters/second
            'humidity': weather_data['main']['humidity'],  # Humidity in percentage
            'pressure': weather_data['main']['pressure'],  # Atmospheric pressure in hPa
        }
    }

    return Response(customized_response, status=status.HTTP_200_OK)