from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import Profile, User
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from django.shortcuts import get_object_or_404
from ..utils import EmailThreading
import logging
from .serializers import (
    CustomAuthTokenSerializer,
    CustomObtainJwtTokenSerializer,
    RegistrationSerializer,
)

logger = logging.getLogger(__name__)


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


class RegistrationApiView(GenericAPIView):
    """ API view for user registration.

        This view handles the registration of a new user. It validates the incoming
        registration data using the `RegistrationSerializer`, saves the new user,
        generates a JWT token for the user, and sends an account verification email
        in a separate thread.
    """

    serializer_class = RegistrationSerializer

    def post(self,request):
        try:
            # Create User object
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # get required data
            email = serializer.validated_data['email']
            user_obj = get_object_or_404(User, email=email)

            # create appropriate data for response
            data = {
                'details': 'User created successfully.',
                'email' : email,
                'note' : 'Verification Email sent. pls verify your account.'
            }

            # create jwt token for activation
            token = self.get_tokens_for_user(user_obj)

            # create message for send activation email
            message = EmailMessage(
                template_name='email/User_activation.tpl',
                context={'user': user_obj, 'token':token},
                from_email= 'admin@admin.com',
                to=[email],

            )
            
            # send email by Threading
            EmailThreading(message).start()
            
            return Response(data,status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_tokens_for_user(self,user):
        """
            Generate a JWT token for the given user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)