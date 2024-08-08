from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from django.shortcuts import get_object_or_404
from ..utils import EmailThreading
import logging
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from ..jwt_utils import (
    ShortLivedAccessToken,
    MediumLivedAccessToken,
    LongLivedAccessToken,
)
from .serializers import (
    CustomAuthTokenSerializer,
    CustomObtainJwtTokenSerializer,
    RegistrationSerializer,
    ActivationResendSerializer,
    ProfileSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
    ChangePasswordSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)


# Profile View
class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        # Assuming each user should only have one profile
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


# Token Based Authentication Views
class CustomObtainAuthToken(ObtainAuthToken):  # login
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        profile = Profile.objects.get(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "user_name": profile.first_name + " " + profile.last_name,
            }
        )


class CustomDiscardAuthToken(APIView):  # logout
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        data = {"details": "User logout successfully."}
        return Response(data)


# Jwt (Json Web Token) Authentication Views
class CustomObtainJwtToken(TokenObtainPairView):
    serializer_class = CustomObtainJwtTokenSerializer


# Registration and Activation User Account
class RegistrationApiView(GenericAPIView):
    """API view for user registration.

    This view handles the registration of a new user. It validates the incoming
    registration data using the `RegistrationSerializer`, saves the new user,
    generates a JWT token for the user, and sends an account verification email
    in a separate thread.
    """

    serializer_class = RegistrationSerializer

    def post(self, request):
        try:
            # Create User object
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # get required data
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)

            # create appropriate data for response
            data = {
                "details": "User created successfully.",
                "email": email,
                "note": "Verification Email sent. pls verify your account.",
            }

            # create jwt token for activation
            token = LongLivedAccessToken.for_user(user_obj)

            # create message for send activation email
            message = EmailMessage(
                template_name="email/User_activation.tpl",
                context={"user": user_obj, "token": token},
                from_email="admin@admin.com",
                to=[email],
            )

            # send email by Threading
            EmailThreading(message).start()

            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ActivationUserConfirmApiView(APIView):
    """
    ActivationUserConfirmApiView handles the confirmation of user account activation through a token-based mechanism.
    This view is designed to validate the activation token, activate the user account if not already activated,
    and provide appropriate feedback to the user.
    """

    def get(self, request, token):
        try:
            token_detail = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response(
                {
                    "error": _(
                        "The activation link has expired. Please request a new activation link."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                {
                    "error": _(
                        "The activation link is invalid. Please check the link and try again."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": _("An unexpected error occurred. Please try again later.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = token_detail.get("user_id")

        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {
                    "error": _(
                        "The user associated with this activation link does not exist."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_obj.is_verified:
            return Response(
                {"info": _("The user account has already been activated.")},
                status=status.HTTP_200_OK,
            )

        user_obj.is_verified = True
        user_obj.save()

        return Response(
            {
                "detail": _(
                    "Your account has been successfully activated. You can now log in."
                )
            },
            status=status.HTTP_200_OK,
        )


class ActivationUserResendApiView(GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user_obj = serializer.validated_data["user"]

        # create jwt token for activation
        token = LongLivedAccessToken.for_user(user_obj)

        # create message for send activation email
        message = EmailMessage(
            template_name="email/User_activation.tpl",
            context={"user": user_obj, "token": token},
            from_email="admin@admin.com",
            to=[email],
        )

        # send email by Threading
        EmailThreading(message).start()

        return Response(
            {"details": "Activation email has been resent successfully."},
            status=status.HTTP_200_OK,
        )


# Reset Password & Reset Password Confirmation
class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user_obj = serializer.validated_data["user"]

        token = ShortLivedAccessToken.for_user(user_obj)

        user_obj.last_password_reset_request = timezone.now()
        user_obj.save()

        reset_url = (
            f"{settings.FRONTEND_URL}/accounts/api/v1/reset-password/confirm/{token}"
        )

        message = EmailMessage(
            template_name="email/reset_password.tpl",
            context={"user": user_obj, "reset_url": reset_url},
            from_email="admin@admin.com",
            to=[email],
        )

        # send email by Threading
        EmailThreading(message).start()

        return Response(
            {"detail": "Password reset email sent."}, status=status.HTTP_200_OK
        )


class ResetPasswordConfirmApiView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data["new_password"]

        try:
            token_detail = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response(
                {
                    "error": _(
                        "The Reset Password link has expired. Please request a new Reset password link."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                {
                    "error": _(
                        "The Reset Password link is invalid. Please check the link and try again."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": _("An unexpected error occurred. Please try again later.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = token_detail.get("user_id")

        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {
                    "error": _(
                        "The user associated with this activation link does not exist."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj.set_password(new_password)
        user_obj.save()

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )


# Change Password
class ChangePasswordApiView(GenericAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.set_password(serializer.validated_data["new_password1"])
            self.object.save()
            response = {
                "status": "success",
                "message": "Password updated successfully",
                # 'data': []
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
