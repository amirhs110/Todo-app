import pytest
from .test_fixture import api_client,user_common,user_verified
from django.urls import reverse

# login Token based Authentication

@pytest.mark.django_db
class TestAccountsTokenLogin:
   
    def test_token_login_verified_user_response(self,api_client,user_verified):
        url = reverse('accounts:token-login')
        data = {
            'email': user_verified.email,
            'password':'123456@mir'
        }
        response = api_client.post(url,data,format='json')
        assert response.status_code == 200
        response_json = response.json()  # Convert response content to JSON
        assert 'token' in response_json  # Check if 'token' key is in the response
        assert response_json['token']  # Optionally, ensure the token is not empty
        assert response_json['user_id'] == user_verified.id

    def test_token_login_unverified_user_response_400_status(self,api_client,user_common):
        url = reverse('accounts:token-login')
        data = {
            'email': user_common.email,
            'password':'123456@mir'
        }
        response = api_client.post(url,data,format='json')
        print(response.content)
        assert response.status_code == 400
