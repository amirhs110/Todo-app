from django.urls import path, include
from .views import CustomLoginView, RegisterView

from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    # add api-v1 urls
    path("api/v1/", include("accounts.api.v1.urls")),
]
