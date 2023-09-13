from rest_framework import serializers
from rest_framework.response import Response
from .models import TarefaModels

class TarefaSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = TarefaModels
        fields  = [
            
            "id",
            "nome",
            "descricao",
            "feita",
            "delete",
            "user"
        ]
        
        def create(self, validated_data):
            return super().create(validated_data)