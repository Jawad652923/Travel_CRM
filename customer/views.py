from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from accounts.permissions import IsAdmin, IsSalesAgent
from .utils import custom_response  

class CustomerViewSet(viewsets.ModelViewSet):
    """
    CustomerViewSet to manage customer data. 
    Admins have full access, while sales agents can only view/update their assigned customers.
    """    
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin | IsSalesAgent]
    queryset = Customer.objects.all()

    def get_queryset(self):
        """
        Admins can access all customers. Sales agents can only access their assigned customers.
        """        
        user = self.request.user
        if user.role == 'admin':
            return Customer.objects.all()
        elif user.role == 'sales_agent':
            return Customer.objects.filter(assigned_sales_agent=user)
        return Customer.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of customers.
        """
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            response_data = custom_response(
                status_code=200,
                message="Customers retrieved successfully.",
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = custom_response(
                status_code=200,
                message='No customers found.',
                data=[]
            )
            return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific customer.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=200,
                message='No customer found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_200_OK)

        user = self.request.user
        if user.role == 'sales_agent' and instance.assigned_sales_agent != user:
            response_data = custom_response(
                status_code=401,
                message='You are not authorized to do this action.',
                data=None
            )
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(instance)
        response_data = custom_response(
            status_code=200,
            message="Customer retrieved successfully.",
            data=serializer.data
        )
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Save the customer with the assigned_sales_agent field set.
        """
        user = self.request.user
        serializer.save(assigned_sales_agent=user)

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new customer.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = custom_response(
                status_code=201,
                message="Customer created successfully.",
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = custom_response(
                status_code=400,
                message="Invalid or missing fields.",
                data=serializer.errors
            )
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        
    def update(self, request, *args, **kwargs):
        """
        Update a customer's data. Admins can update any customer, while sales agents can only update their assigned customers.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = self.request.user
        if user.role == 'sales_agent' and instance.assigned_sales_agent != user:
            response_data = custom_response(
                status_code=403,
                message='You do not have permission to update this customer.',
                data=None
            )            
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = custom_response(
                status_code=200,
                message="Customer updated successfully.",
                data=serializer.data
            )            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = custom_response(
                status_code=400,
                message="Invalid data provided.",
                data=serializer.errors
            )            
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a customer's data. Admins can update any customer, while sales agents can only update their assigned customers.
        """        
        instance = self.get_object()
        user = self.request.user
        if user.role == 'sales_agent' and instance.assigned_sales_agent != user:
            response_data = custom_response(
                status_code=403,
                message='You do not have permission to update this customer.',
                data=None
            )            
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        partial = True
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = custom_response(
                status_code=200,
                message="Customer updated successfully.",
                data=serializer.data
            )            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = custom_response(
                status_code=400,
                message="Invalid data provided.",
                data=serializer.errors
            )            
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Only the admin can delete a customer. Sales agents are not allowed to delete customers.
        """        
        instance = self.get_object()
        user = self.request.user
        if user.role == 'admin':
            instance.delete()
            response_data = custom_response(
                status_code=200,
                message="Customer successfully deleted.",
                data=None
            )            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = custom_response(
                status_code=403,
                message='Sales agents are not allowed to delete customers.',
                data=None
            )
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
