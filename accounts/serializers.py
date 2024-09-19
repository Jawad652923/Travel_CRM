from rest_framework import serializers
from .models import CustomUser

class SalesAgentSerializer(serializers.ModelSerializer):
        """
        Serializer for creating a new sales agent user with optional role specification.

        This serializer handles the creation of sales agent users and can optionally
        accept the `role` field from the payload.

        Fields:
            - username (str): The username of the sales agent.
            - email (str): The email address of the sales agent.
            - password (str): The password for the sales agent's account.
            - role (str): The role assigned to the user (optional, default to 'sales_agent').

        Extra kwargs:
            - password (dict): Ensures that the password is write-only and not included
            in the serialized output.

        Methods:
            - create(validated_data): Creates a new sales agent user with the provided
            validated data.
            
        Meta:
            model (CustomUser): The model associated with this serializer.
            fields (list): List of fields to include in the serialized representation.
        """
        class Meta:
            model = CustomUser
            fields = ['username', 'email', 'password', 'role']
            extra_kwargs = {
                'password': {'write_only': True},
            }

        def create(self, validated_data):
            """
            Create a new user with the specified role.

            Args:
                validated_data (dict): The validated data from the serializer containing
                'username', 'email', 'password', and optionally 'role'.

            Returns:
                CustomUser: The newly created user instance.
            """
            role = validated_data.get('role', 'sales_agent')  # Default role if not specified
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=role
            )
            return user
