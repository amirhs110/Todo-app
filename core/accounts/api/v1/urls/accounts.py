from django.urls import path
from ..views import (
    CustomObtainAuthToken,
    CustomDiscardAuthToken,
    CustomObtainJwtToken,
    RegistrationApiView,
    ActivationUserConfirmApiView,
    ActivationUserResendApiView,
    ResetPasswordApiView,
    ResetPasswordConfirmApiView,
    ChangePasswordApiView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Token Based Authentication
    # login
    path("token/login/", CustomObtainAuthToken.as_view(), name="token-login"),
    # logout
    path("token/logout/", CustomDiscardAuthToken.as_view(), name="token-logout"),
    # Jwt (Json Web Token) authentication
    # create
    path("jwt/create/", CustomObtainJwtToken.as_view(), name="jwt-create"),
    # refresh
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    # verify
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # User Registration & Activation
    # registration
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    # activation
    path(
        "activation/confirm/<str:token>",
        ActivationUserConfirmApiView.as_view(),
        name="activation-confirm",
    ),
    # resend-activation
    path(
        "activation/resend/",
        ActivationUserResendApiView.as_view(),
        name="activation-resend",
    ),
    # Change Password
    path("change-password/", ChangePasswordApiView.as_view(), name="change-password"),
    # Reset Password
    # reset
    path("reset-password/", ResetPasswordApiView.as_view(), name="reset-password"),
    # reset-confirm
    path(
        "reset-password/confirm/<str:token>",
        ResetPasswordConfirmApiView.as_view(),
        name="reset-password-confirm",
    ),
]
