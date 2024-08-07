from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from accounts.models import User , Profile
from django.contrib.auth.password_validation import validate_password


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'description', 'image']
        read_only_fields = ['user']

    def to_representation(self, instance):
        repo = super().to_representation(instance)

        repo['user'] = {
            'user_id': instance.user.id,
            'email' : instance.user.email,
        }
        return repo

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user.is_verified:
                msg = _('User is not verified.')
                raise serializers.ValidationError(msg, code='authorization')
        
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomObtainJwtTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            msg = _('User is not verified.')
            raise ValidationError(msg)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_id"]= self.user.id
        data["user_email"]= self.user.email

        return data
    

class RegistrationSerializer(ModelSerializer):
    re_password = serializers.CharField(max_length=128,write_only=True,required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 're_password')
    
    def validate(self, attrs):
        # get attributes
        email = attrs.get('email')
        password = attrs.get('password')
        re_pass = attrs.get('re_password') 

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            msg = _("A user with this email already exists.")
            raise serializers.ValidationError({'email': msg})

        # Checking the similarity of two passwords
        if password != re_pass:
            msg = _("password doesn't match")
            raise serializers.ValidationError({'error': msg })
        
        # check validation of entered password
        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('re_password')
        return User.objects.create_user(**validated_data)
    

class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            msg = _("A user with this email does not exist.")
            raise serializers.ValidationError({'error': msg})

        if user_obj.is_verified:
            msg = _("The user account has already been activated.")
            raise serializers.ValidationError({'email': msg})
        
        attrs['user'] = user_obj

        return super().validate(attrs)



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('A user with this email does not exist.'))

        if not user_obj.is_verified:
            msg = _("The user is not verified.")
            raise serializers.ValidationError({'error': msg})
        
        # This approach ensures that users cannot flood the system with password reset requests.
        cooldown_period = timedelta(minutes=10)  # cooldown period

        if user_obj.last_password_reset_request and timezone.now() - user_obj.last_password_reset_request < cooldown_period:
            raise serializers.ValidationError(_('You can only request a password reset once every 10 minutes.'))


        attrs['user'] = user_obj
        return super().validate(attrs)

class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True,required=True)
    re_new_password = serializers.CharField(write_only=True,required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        re_new_password = attrs.get('re_new_password')
    
        if new_password != re_new_password:
            raise serializers.ValidationError(_('Passwords do not match.'))

        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})

        return super().validate(attrs)
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, required=True, write_only=True
    )
    new_password1 = serializers.CharField(
        max_length=128, required=True, write_only=True
    )
    new_password2 = serializers.CharField(
        max_length=128, required=True, write_only=True
    )

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs.get("old_password")):
            raise serializers.ValidationError(
                _(
                    "Your old password was entered incorrectly. Please enter it again."
                )
            )

        if attrs.get("new_password1") != attrs.get("new_password2"):
            raise serializers.ValidationError(
                {"detail": "password doesn't match"}
            )

        try:
            validate_password(attrs.get("new_password1"))
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)