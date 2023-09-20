from django.shortcuts import render
from django.http import Http404
from .serializers import userSerializer, CustomTonkenObtationParirSerializer, userUpdateSerializer, userListeSerializer
from rest_framework import generics
from rest_framework.views import APIView
from .models import userModels
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .middlewares import Middlewares
from .permissions import ValidToken, ValidAdmin
from django.contrib.auth.hashers import make_password
# Create your views here.

class CreateUserView(generics.CreateAPIView): #  criar usuario
    
    model = userModels 
    
    serializer_class = userSerializer

class CustomTokenobtainPairView(TokenObtainPairView): #  constonisar token e permitir que ele faça o login
    
    serializer_class = CustomTonkenObtationParirSerializer

class LogoutView(APIView):
    
    permission_classes = [ValidToken]
    
    queryset = userModels.objects.all()                
    
    def post(self, resquest):
        
        refresh_token = resquest.data.get('refresh_token')
        
        if refresh_token:
            
            try:
                
                token = RefreshToken(refresh_token)
                token.blacklist()
                
                return Response({'detail': "Logout realizado com sucesso!"}, status = 200)
            
            except Exception as e:
                
                return Response({'detail': "Erro ao fazer logout!"}, status = 400)
        
        return Response({'detail':"O token de autenticação (resfresh_token) é necessario para fazer o logout"}, status = 400)
    
class UserViewPrivate(APIView):
    
    permission_classes = [ValidToken]
    queryset = userModels.objects.all()
    
    def get_queryset(self, pk):
        
        try:
            
            return self.queryset.get(pk=pk)
        
        except userModels.DoesNotExist:
            
            raise Http404
        
    def put(self, request): 
        
        user_id = Middlewares.decode(request.headers)
        tipo = self.get_queryset(user_id)
        data = userSerializer(tipo).data 
        
        #if (user_id == id):
            
        menssagem = 'Changed not password'
        user = self.get_queryset(user_id)
        userAnt = serializer = userSerializer(user)
        data = request.data
        
        try:
            
            if (data["password"] and user.check_password(data['password_back'])):
                data['password'] = make_password(data("password"))
                user.set_password(data['password'])
                menssagem = "Changed password"
                
        
        except:
            
            menssagem = 'Changed not password'
            data['password'] = user.password
            
        serializer = userUpdateSerializer(user, data=data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response({"detail": "Atualizado com sucesso", "menssagem" : menssagem}, status = 200)
        
        return Response(serializer.erro, status = 404)
        #else:
          #  return response({"deital" : "Não autorizado!"})
          
class AdminView(APIView):
    
    permission_classes = [ValidToken,ValidAdmin]
    queryset = userModels.objects.all()
    
    def get_object(self, pk, tipo): 
        
        try:
            return self.queryset.get(pk=pk, tipo = tipo)
        except userModels.DoesNotExist:
            return Http404
    
    def get(self, request, id = None): #trazer um ou varios usuatios
        
        if id is not None:
            user = self.get_object(id, tipo = "client")
            serializer = userListeSerializer(user)
            
        else:
            
            users = self.queryset.filter(tipo = "client")
            serializer = userListeSerializer(users, many = True)
            
            return Response(serializer.data)
        
    def patch(self, request, id):
        
        user  = self.get_object(id, tipo = "client")
        serializer = userSerializer(user, data = request.data,  partial = True)
        
        if serializer.is_valid():
            serializer.save()
            
            serializer = userUpdateSerializer(serializer.data)
            return Response(serializer.data, status = 200)
        return Response(serializer.errors, status = 400)
