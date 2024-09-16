from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Create serializer for an 'admin'.
    """
    class Meta:
        model = CustomUser
        fields = ['id','username','email','role']
        
        
class SalesAgentSerializer(serializers.ModelSerializer):
    """
    Create serializer for adding user such as 'sales_agent'.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='sales_agent'  
        )
        return user