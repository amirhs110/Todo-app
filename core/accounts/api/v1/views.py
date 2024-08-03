from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CustomAuthTokenSerializer


 # Token Based Authentication Views
class CustomObtainAuthToken(ObtainAuthToken):  # login
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.id,
                'user': user.first_name +" "+ user.last_name,
                'email': user.email
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

