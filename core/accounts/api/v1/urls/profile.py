from django.urls import path, include
from ..views import ProfileApiView

urlpatterns = [
    # Profile
    path('', ProfileApiView.as_view(), name='profile'),
]
