from rest_framework import serializers
from .models import Inquiries
from customer.models import Customer
from services.models import Service
from accounts.models import CustomUser
from customer.serializers import CustomerSerializer
from services.serializers import ServiceSerializer
from accounts.serializers import SalesAgentSerializer

class InquirySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # Use ID for input
    assigned_sales_agent = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)  # Use ID for input
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)  # Use ID for input

    class Meta:
        model = Inquiries
        fields = ['id', 'details', 'status', 'customer', 'assigned_sales_agent', 'services']

    def create(self, validated_data):
        # Handle the creation of Inquiry instance
        customer = validated_data.pop('customer')
        services = validated_data.pop('services')

        inquiry = Inquiries.objects.create(customer=customer, **validated_data)
        
        # Add services to the inquiry
        inquiry.services.set(services)

        return inquiry

    def update(self, instance, validated_data):
        # Update Inquiry instance fields
        instance.details = validated_data.get('details', instance.details)
        instance.status = validated_data.get('status', instance.status)
        
        # Handle the update of customer and services
        if 'customer' in validated_data:
            instance.customer = validated_data['customer']

        if 'assigned_sales_agent' in validated_data:
            instance.assigned_sales_agent = validated_data['assigned_sales_agent']
        
        if 'services' in validated_data:
            instance.services.set(validated_data['services'])
        
        instance.save()
        return instance

    def to_representation(self, instance):
        # Customize the representation of Inquiry instance
        representation = super().to_representation(instance)
        representation['customer'] = CustomerSerializer(instance.customer).data
        representation['assigned_sales_agent'] = SalesAgentSerializer(instance.assigned_sales_agent).data if instance.assigned_sales_agent else None
        representation['services'] = ServiceSerializer(instance.services.all(), many=True).data
        return representation
