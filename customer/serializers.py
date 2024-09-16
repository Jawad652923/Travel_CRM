from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer fields and add assgined_sale_agent field on read only 
    to automatically add when they create customer.
    """

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_no', 'address', 'assigned_sales_agent']
        read_only_fields = ['assigned_sales_agent']
