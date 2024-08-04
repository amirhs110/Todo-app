from django.urls import path, include
from ..views import (
    CustomObtainAuthToken,
    CustomDiscardAuthToken,
    CustomObtainJwtToken,
    RegistrationApiView,
    ActivationUserConfirmApiView,
    ActivationUserResendApiView,
    ResetPasswordApiView,
    ResetPasswordConfirmApiView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Token Based Authentication
        # login
    path('token/login/', CustomObtainAuthToken.as_view(), name='token-login'),
        # logout
    path('token/logout/', CustomDiscardAuthToken.as_view(), name='token-logout'),


    # Jwt (Json Web Token) authentication
        # create
    path('jwt/create/', CustomObtainJwtToken.as_view(), name='jwt-create'),
        # refresh
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
        # verify
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),


    # User Registration & Activation
        # registration
    path('registration/', RegistrationApiView.as_view(), name='registration'),
        # activation
    path('activation/confirm/<str:token>', ActivationUserConfirmApiView.as_view(), name='activation-confirm'),
        # resend-activation
    path('activation/resend/', ActivationUserResendApiView.as_view(), name='activation-resend'),


    # Reset Password
        # reset
    path('reset-password/', ResetPasswordApiView.as_view(), name='reset-password'),
        # reset-confirm
    path('reset-password/confirm/<str:token>', ResetPasswordConfirmApiView.as_view(), name='reset-password-confirm'),

]
