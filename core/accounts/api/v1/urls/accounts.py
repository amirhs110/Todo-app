from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    # Token Based Authentication
        # login
    path('token-login/', ObtainAuthToken.as_view()),

        # logout

    # Jwt (Json Web Token) authentication
        # create
        # refresh
        # verify

    # User Registration & Activation
        # registration
        # activation
        # resend-activation

    # Reset Password
        # reset
        # reset-confirm
        
]
