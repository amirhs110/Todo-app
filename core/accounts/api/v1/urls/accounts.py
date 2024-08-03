from django.urls import path, include
from ..views import (
    CustomObtainAuthToken,
    CustomDiscardAuthToken,
)


urlpatterns = [
    # Token Based Authentication
        # login
    path('token/login/', CustomObtainAuthToken.as_view()),
        # logout
    path('token/logout/', CustomDiscardAuthToken.as_view()),

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
