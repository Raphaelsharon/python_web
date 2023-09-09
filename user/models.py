from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

# Create your models here.

class userModels(AbstractUser):
    
    tipo_choice = [
        ("root", "Root"),
        ("client", "Client")
    ]
    
    id = models.UUIDField(primary_key= True, default = uuid4, editable = False) 
    suspenso = models.BooleanField(default = False)
    email = models.EmailField(unique = True)
    tipo = models.CharField(max_length = 10, choices = tipo_choice, default = "client")