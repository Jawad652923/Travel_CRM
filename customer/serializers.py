from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_no', 'address', 'assigned_sales_agent']
        read_only_fields = ['assigned_sales_agent']
