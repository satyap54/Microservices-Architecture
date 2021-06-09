from django.contrib import auth
from django.db import models
from rest_framework import serializers
from . models import User
from django.contrib.auth import authenticate
from . settings import api_settings
from django.contrib.auth.models import update_last_login


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password':{
                'write_only': True, 
                'style': {
                    'input_type': 'password',
                },
            },
        }
        
    def create(self, data):
        user = User.objects.create_user(
            email = data['email'],
            name = data['name'],
            password = data['password'],
        )
        return user
        
    
class UserLoginSerializer(serializers.Serializer):
    
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=20, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if(user is None):
            raise serializers.ValidationError(
                'No such email'
            )
        
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            payload["user_handle"] = user.name
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Invalid email or password'
            )
        print(payload)
        return{
            'email': user.email,
            'token': jwt_token,
        }