import pytest
from .test_fixture import api_client, user_common, user_verified, jwt_refresh_token
from django.urls import reverse

# Jwt (Json Web Token) authentication


@pytest.mark.django_db
class TestAccountsJwtAuth:

    def test_jwt_create_verified_user_response(self, api_client, user_verified):
        url = reverse("accounts:jwt-create")
        data = {"email": user_verified.email, "password": "123456@mir"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200
        response_json = response.json()
        assert "refresh" in response_json
        assert response_json["refresh"]
        assert response_json["user_id"] == user_verified.id

    def test_jwt_refresh_verified_user_response(
        self, api_client, user_verified, jwt_refresh_token
    ):
        token = jwt_refresh_token
        url = reverse("accounts:jwt-refresh")
        data = {"refresh": token}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200
        response_json = response.json()
        assert "access" in response_json

    def test_jwt_verify_user_response(
        self, api_client, user_verified, jwt_refresh_token
    ):
        token = jwt_refresh_token
        url = reverse("accounts:jwt-verify")
        data = {"token": token}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200
