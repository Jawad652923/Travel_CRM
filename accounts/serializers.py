from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Create serializer for users such as 'admin' or 'sales_agent'
    """
    class Meta:
        model = CustomUser
        fields = ['id','username','email','role']