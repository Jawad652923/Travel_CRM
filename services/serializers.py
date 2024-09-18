from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.

    This serializer converts `Service` instances to JSON and validates JSON data for creating or updating `Service` instances.

    Attributes:
        id (int): The unique identifier of the service.
        name (str): The name of the service.
        description (str): A detailed description of the service.
        price (str): The price of the service. Can be null or blank.

    Methods:
        create(validated_data): Creates a new `Service` instance using the validated data.
        update(instance, validated_data): Updates an existing `Service` instance with the validated data.
    """

    class Meta:
        model = Service
        fields = ['id', 'name', 'description','price']
