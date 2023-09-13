from django.conf import settings
import jwt
from rest_framework import permissions
from user.models import userModels

class IsNotSuspended(permissions.BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        return not user.suspenso
    
def validate_token(token):
        
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = ['HS256'])
        user = userModels.objects.filter(id=payload['user_id']).first()
        print(user)
        
            
        if not user:
            return False
            
        user.refresh_from_db()
        
        return user
    except Exception as e:
            return False

def has_user_permission(user, path):
        user_id = path.split('/')[-3]
        
        return str(user.id) == user_id and not user.is_blocked
    
class ValidToken(permissions.BasePermission):
    def has_permission(self, request, path):
        
        token = request.headers.get('token')
        user = validate_token(token)
        print(user)
        
        if not user:
            return False
        
        request.user = user
        
        return True
    
class ValidAdmin(permissions.BasePermission):
    
    def has_permission(self, resquet, view):
        
        try:
            
            token = resquet.headers.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms = ['HS256'])
            user = userModels.objects.filter(id= payload['user_id'], tipo= "root").first()
            print("teste")
            print(user)
            
            if not user: 
                return False
            
            resquet.user = user
            return True 
        except Exception as e:
            return False