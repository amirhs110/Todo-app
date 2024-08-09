import pytest
from .test_fixture import api_client, user_common, user_verified, jwt_refresh_token
from django.urls import reverse

# Change password and Reset password


@pytest.mark.django_db
class TestAccountsPassword:

    def test_change_password_user_response_200_status(self, api_client, user_verified):
        url = reverse("accounts:change-password")
        api_client.force_authenticate(user=user_verified)
        data = {
            "old_password": "123456@mir",
            "new_password1": "123456789@mir",
            "new_password2": "123456789@mir",
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 200

    def test_change_password_user_response_400_status(self, api_client, user_verified):
        url = reverse("accounts:change-password")
        api_client.force_authenticate(user=user_verified)
        data = {
            "old_password": "123456@mir",
            "new_password1": "123456789@mir",
            "new_password2": "123456789",
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 400
        response_json = response.json()
        assert response_json["detail"] == ["password doesn't match"]

    def test_reset_password_verified_user_response_200_status(
        self, api_client, user_verified
    ):
        url = reverse("accounts:reset-password")
        data = {"email": user_verified.email}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200

    def test_reset_password_unverified_user_response_400_status(
        self, api_client, user_common
    ):
        url = reverse("accounts:reset-password")
        data = {"email": user_common.email}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 400

    def test_reset_password_confirm_response_200_status(
        self, api_client, jwt_refresh_token
    ):
        # Generate the activation token
        token = jwt_refresh_token

        # Generate the URL
        url = reverse("accounts:reset-password-confirm", kwargs={"token": token})

        data = {"new_password": "123456789@mir", "re_new_password": "123456789@mir"}

        # Send the activation request
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200

        response_json = response.json()
        assert response_json["detail"] == "Password has been reset successfully."
