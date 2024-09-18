from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and displaying user data for admins.

    Fields:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        role (str): The role assigned to the user (e.g., 'admin', 'sales_agent').

    Meta:
        model (CustomUser): The model associated with this serializer.
        fields (list): List of fields to include in the serialized representation.
    """
    class Meta:
        model = CustomUser
        fields = ['id','username','email','role']
        
        
class SalesAgentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and adding a new sales agent user.

    Fields:
        username (str): The username of the sales agent.
        email (str): The email address of the sales agent.
        password (str): The password for the sales agent's account.
        role (str): The role assigned to the user, which is set to 'sales_agent'.

    Extra kwargs:
        password (dict): Ensures that the password is write-only and not included in the serialized output.

    Methods:
        create(validated_data): Creates a new sales agent user with the provided validated data.
        
    Meta:
        model (CustomUser): The model associated with this serializer.
        fields (list): List of fields to include in the serialized representation.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Create a new sales agent user.

        Args:
            validated_data (dict): The validated data from the serializer containing 'username', 'email', and 'password'.

        Returns:
            CustomUser: The newly created sales agent user instance.
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='sales_agent'  
        )
        return user