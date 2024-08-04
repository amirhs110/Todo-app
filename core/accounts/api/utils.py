from collections.abc import Callable
import threading
from typing import Any, Iterable, Mapping
import logging
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

class EmailThreading(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.email_message.send()
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

class CustomAccessToken(AccessToken):
    """
        Extend the AccessToken class to allow setting a custom expiration time.
    """
    def set_exp(self, lifetime):
        self.set_exp(from_time=timezone.now(), lifetime=lifetime)


def generate_activation_token(user): # For activation token
    # Set the custom lifetime for the activation token
    access_token = CustomAccessToken.for_user(user)
    access_token.set_exp(lifetime=timedelta(days=1))
    return str(access_token)

def generate_password_reset_token(user):  # For password reset token
    # Set the custom lifetime for the password reset token
    access_token = CustomAccessToken.for_user(user)
    access_token.set_exp(lifetime=timedelta(hours=1))
    return str(access_token)

def generate_access_token(user):  # For regular access token
    # Default token lifetime from settings
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)