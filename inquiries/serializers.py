from rest_framework import serializers
from .models import Inquiries
from customer.models import Customer
from services.models import Service
from accounts.models import CustomUser
from customer.serializers import CustomerSerializer
from services.serializers import ServiceSerializer
from accounts.serializers import SalesAgentSerializer

class InquirySerializer(serializers.ModelSerializer):
    """
    Serializer for handling Inquiry instances, including creation, updating, and representation.

    Attributes:
        customer (PrimaryKeyRelatedField): Represents the ID of the customer making the inquiry.
        assigned_sales_agent (PrimaryKeyRelatedField, optional): Represents the ID of the sales agent assigned to the inquiry.
        services (PrimaryKeyRelatedField): Represents the IDs of the services related to the inquiry.

    Meta:
        model (Inquiries): The model associated with this serializer.
        fields (list): List of fields to be included in the serialization and deserialization processes.

    Methods:
        create(validated_data): Handles the creation of an Inquiry instance and associates the provided services.
        update(instance, validated_data): Updates an existing Inquiry instance with the provided data.
        to_representation(instance): Customizes the representation of an Inquiry instance to include nested serialized data for customer, assigned_sales_agent, and services.
    """
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all()) 
    assigned_sales_agent = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)  

    class Meta:
        model = Inquiries
        fields = ['id', 'details', 'status', 'customer', 'assigned_sales_agent', 'services']

    def create(self, validated_data):
        """
        Create a new Inquiry instance with the provided data and associate the services.

        Args:
            validated_data (dict): The validated data for creating the Inquiry.

        Returns:
            Inquiry: The newly created Inquiry instance.
        """
        customer = validated_data.pop('customer')
        services = validated_data.pop('services')

        inquiry = Inquiries.objects.create(customer=customer, **validated_data)
        inquiry.services.set(services)
        return inquiry

    def update(self, instance, validated_data):
        """
        Update an existing Inquiry instance with the provided data.

        Args:
            instance (Inquiry): The Inquiry instance to update.
            validated_data (dict): The validated data for updating the Inquiry.

        Returns:
            Inquiry: The updated Inquiry instance.
        """
        instance.details = validated_data.get('details', instance.details)
        instance.status = validated_data.get('status', instance.status)
        
        if 'customer' in validated_data:
            instance.customer = validated_data['customer']

        if 'assigned_sales_agent' in validated_data:
            instance.assigned_sales_agent = validated_data['assigned_sales_agent']
        
        if 'services' in validated_data:
            instance.services.set(validated_data['services'])
        
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Customize the representation of the Inquiry instance to include nested serialized data.

        Args:
            instance (Inquiry): The Inquiry instance to serialize.

        Returns:
            dict: A dictionary representation of the Inquiry instance with nested data.
        """        
        representation = super().to_representation(instance)
        representation['customer'] = CustomerSerializer(instance.customer).data
        representation['assigned_sales_agent'] = SalesAgentSerializer(instance.assigned_sales_agent).data if instance.assigned_sales_agent else None
        representation['services'] = ServiceSerializer(instance.services.all(), many=True).data
        return representation
