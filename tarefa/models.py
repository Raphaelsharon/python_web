from django.db import models
from uuid import uuid4
from user.models import userModels 
# Create your models here.

class tarefaModels(models.Model):
    
    id = models.UUIDField(primary_key= True, default = uuid4, editable = False)
    user = models.ForeignKey(userModels, on_delete = models.CASCADE, related_name = "tarefa")
    nome = models.CharField(max_length = 254)
    descricao = models.CharField(max_length = 254)
    feita = models.BooleanField(default = False)
    delete = models.BooleanField(default = False)
    creat_at = models.DateTimeField(auto_now_add = True)