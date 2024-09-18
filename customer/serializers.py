from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.

    Handles serialization and deserialization of Customer instances, including:
    - `id`: The unique identifier for the customer.
    - `name`: The full name of the customer.
    - `email`: The email address of the customer.
    - `phone_no`: The phone number of the customer.
    - `address`: The residential address of the customer.
    - `assigned_sales_agent`: The sales agent assigned to this customer. This field is read-only.

    Fields:
        - `id` (int): The unique identifier of the customer.
        - `name` (str): The full name of the customer.
        - `email` (str): The email address of the customer.
        - `phone_no` (str): The phone number of the customer.
        - `address` (str): The residential address of the customer.
        - `assigned_sales_agent` (CustomUser): The sales agent assigned to this customer. This field is read-only.

    Read-Only Fields:
        - `assigned_sales_agent`: This field is set automatically when a customer is created and cannot be modified through this serializer.
    """
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_no', 'address', 'assigned_sales_agent']
        read_only_fields = ['assigned_sales_agent']
