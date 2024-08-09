from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken


class ShortLivedAccessToken(AccessToken):
    """
    Custom Access Token class with a short lifetime of 5 minutes.

    This class is used to generate access tokens that expire after 5 minutes.
    Suitable for scenarios where a short-lived token is required for security reasons.
    """

    token_type = "access"
    lifetime = timedelta(minutes=5)


class MediumLivedAccessToken(AccessToken):
    """
    Custom Access Token class with a medium lifetime of 1 hour.

    This class is used to generate access tokens that expire after 1 hour.
    Suitable for scenarios where an access token with moderate longevity is needed.
    """

    token_type = "access"
    lifetime = timedelta(hours=1)


class LongLivedAccessToken(AccessToken):
    """
    Custom Access Token class with a long lifetime of 1 day.

    This class is used to generate access tokens that expire after 1 day.
    Suitable for scenarios where a long-lived token is required.
    """

    token_type = "access"
    lifetime = timedelta(days=1)
