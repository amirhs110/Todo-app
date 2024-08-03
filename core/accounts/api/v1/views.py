from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import Profile
from .serializers import (
    CustomAuthTokenSerializer,
    CustomObtainJwtTokenSerializer,
)

 # Token Based Authentication Views
class CustomObtainAuthToken(ObtainAuthToken):  # login
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        profile = Profile.objects.get(user=user)

        return Response(
            {
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'user_name': profile.first_name + " " + profile.last_name,
            }
        )
    

class CustomDiscardAuthToken(APIView):  # logout
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        data = {
            'details': 'User logout successfully.'
        }
        return Response(data)


# Jwt (Json Web Token) Authentication Views
class CustomObtainJwtToken(TokenObtainPairView):
    serializer_class = CustomObtainJwtTokenSerializer