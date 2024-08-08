import pytest
from rest_framework.test import APIClient
from accounts.models import User, Profile
from django.urls import reverse

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
def user_profile(user_common):
    profile = Profile.objects.create(
            user= user_common,
            first_name='test_first_name',
            last_name="test_last_name",
            description = "Hello World",
        )
    return profile


@pytest.mark.django_db
class TestPostAPi:

    def test_get_task_list_verified_user_response_200_status(self,api_client,user_verified):
        """
        status code 200: get post list correctly with get request
        """
        url = reverse("task:api-v1:task-list")
        api_client.force_authenticate(user=user_verified)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_task_list_unverified_user_response_403_status(self,api_client,user_common):
        """
        status code 403: Forbidden responses, authenticating or re-authenticating makes no difference.
        """
        url = reverse("task:api-v1:task-list")
        api_client.force_authenticate(user=user_common)
        response = api_client.get(url)
        assert response.status_code == 403

    def test_create_task_response_201_status(self,api_client,user_verified):
        """
        status code 201: create a task with given user and data correctly
        """
        url = reverse("task:api-v1:task-list")
        data = {
            "title" : "test_title",
            "content" : "description",
        }
        api_client.force_authenticate(user=user_verified)
        response = api_client.post(url,data, format='json')
        assert response.status_code == 201

    def test_create_task_response_400_status(self,api_client,user_verified):
        """
        status code 400: Don't create task
            because we send authenticated user but with wrong task data 
        """
        url = reverse("task:api-v1:task-list")
        data = {
            "content" : "description"
        }
        api_client.force_authenticate(user=user_verified)
        response = api_client.post(url,data, format='json')
        assert response.status_code == 400
        # check the response data
        response_json = response.json()
        assert response_json['title'] == ["This field is required."]