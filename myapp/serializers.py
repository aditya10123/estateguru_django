from rest_framework import serializers
from .models import customer_details



class properserializer(serializers.ModelSerializer):
    class Meta:
        model=customer_details
        fields='__all__'

        
    