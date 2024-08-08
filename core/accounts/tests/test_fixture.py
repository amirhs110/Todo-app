import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, Profile
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def user_common():
    user_obj = User.objects.create_user(email="test@test.com",password="123456@mir")
    return user_obj

@pytest.fixture
def user_verified():
    user_obj = User.objects.create_user(email="test@test.com",password="123456@mir", is_verified=True)
    return user_obj

@pytest.fixture
def user_profile_verified(user_verified):
    profile = Profile.objects.create(
            user= user_verified,
            first_name='test_first_name',
            last_name="test_last_name",
            description = "Hello World",
        )
    return profile


@pytest.fixture
def jwt_token(user_common):
    refresh = RefreshToken.for_user(user_common)
    return str(refresh.access_token)