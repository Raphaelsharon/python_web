from rest_framework import serializers
from .models import userModels
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class CustomTonkenObtationParirSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.suspenso:
            raise AuthenticationFailed("Conta está suspensa")
        
        token = super().get_token(user)
        token['user_id'] = str(user.id)
        token["username"] = user.username
        token['email'] = user.email
        token['tipo'] = user.tipo
        token['suspenso'] = user.suspenso
        
        return token
    
class userSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True,
                                     required = True)
    token = serializers.SerializerMethodField()
    class Meta:
        model = userModels
        fields = [
            'id', 
            'username', 
            'email', 
            'password', 
            'tipo', 
            'suspenso',
            'token'
        ]
        
    def get_token(self, user):
            
        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = str(user.id)
        refresh["username"] = user.username
        refresh['email'] = user.email
        refresh['tipo'] = user.tipo
        refresh['suspenso'] = user.suspenso
        
        
    def create(self, validated_date):
        
        validated_date['password'] = make_password(validated_date.get("password"))
        validated_date['tipo'] = 'client'
        
        user = super().create(validated_date)
        user.token = self.get_token(user)
        
        return user
        
class userListeSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = userModels
        fields = ["id",'username', 'email', 'tipo', 'suspenso']
        
class userUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = userModels
        fields = ['username', 'email', 'password']
    
    username = serializers.CharField(required= False)
    email = serializers.EmailField(required= False)
    password = serializers.CharField(required= False)
    
    