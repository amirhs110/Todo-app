import pytest
from .test_fixture import api_client,user_common,jwt_token
from django.urls import reverse

# Registration and Activation user

@pytest.mark.django_db
class TestAccountsRegistration:

    def test_registration_user_valid_data_response_201_status(self,api_client):
        url = reverse('accounts:registration')
        data = {
            'email': "test@test.com",
            'password':'123456@mir',
            're_password':'123456@mir'
        }
        response = api_client.post(url,data,format='json')
        assert response.status_code == 201

    def test_registration_user_invalid_data_response_400_status(self,api_client):
        url = reverse('accounts:registration')
        data = {
            'email': "test@test.com",
            'password':'123',
            're_password':'123'
        }
        response = api_client.post(url,data,format='json')
        assert response.status_code == 400

    def test_activation_user_response_200_status(self, api_client, user_common, jwt_token):
        # Generate the activation token
        token = jwt_token
        
        # Generate the URL
        url = reverse('accounts:activation-confirm', kwargs={'token': token})
        
        # Send the activation request
        response = api_client.get(url)
        assert response.status_code == 200
        
        # Refresh the user from the database
        # Refreshing the user from the database ensures
        #  that you are getting the latest state of the user object 
        user_common.refresh_from_db()
        
        # Check if the user is now verified
        assert user_common.is_verified
        response_json = response.json()
        assert response_json['detail'] == "Your account has been successfully activated. You can now log in."

    def test_activation_user_invalid_token_response_400_status(self, api_client, user_common, jwt_token):
        # Generate the activation token
        token = jwt_token
        
        # Generate the URL
        url = reverse('accounts:activation-confirm', kwargs={'token': None})
        
        # Send the activation request
        response = api_client.get(url)
        assert response.status_code == 400
        response_json = response.json()
        assert response_json['error'] == "The activation link is invalid. Please check the link and try again."