from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from accounts.permissions import IsAdmin, IsSalesAgent
from .utils import custom_response  

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Customer data.

    Admins have full access to all customer data, while sales agents have restricted access:
    - Sales agents can only view and manage customers they are assigned to.
    - Sales agents cannot delete customers.
    """
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin | IsSalesAgent]
    queryset = Customer.objects.all()

    def get_queryset(self):
        """
        Return the queryset for listing or retrieving customer data.

        Admins can access all customer records.
        Sales agents can only access customer records assigned to them.

        Returns:
            QuerySet: A queryset of customers based on the user's role.
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

        Admins can retrieve all customer records.
        Sales agents can retrieve only their assigned customers.

        Returns:
            Response: A response containing the list of customers or a message if no customers are found.
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
                status_code=404,
                message='No customers found.',
                data=[]
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific customer.

        Admins can view any customer record.
        Sales agents can view only customers assigned to them.

        Returns:
            Response: A response containing the customer details or a message if the customer is not found.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='No customers found.',
                data=[]
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        response_data = custom_response(
            status_code=200,
            message="Customer retrieved successfully.",
            data=serializer.data
        )
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Save a new customer instance.

        Sets the `assigned_sales_agent` field to the current user.

        Args:
            serializer (CustomerSerializer): The serializer instance used to validate and save the customer data.
        """
        user = self.request.user
        serializer.save(assigned_sales_agent=user)

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new customer.

        Validates the input data and saves a new customer record.

        Returns:
            Response: A response indicating the result of the creation attempt, including success or error details.
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
        Update an existing customer record.

        Admins can update any customer record.
        Sales agents can only update customers assigned to them.

        Args:
            request (Request): The request object containing the update data.

        Returns:
            Response: A response indicating the result of the update attempt, including success or error details.
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
        Partially update an existing customer record.

        Admins can update any customer record.
        Sales agents can only partially update customers assigned to them.

        Args:
            request (Request): The request object containing the partial update data.

        Returns:
            Response: A response indicating the result of the partial update attempt, including success or error details.
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
        Delete a customer record.

        Only admins can delete customer records. Sales agents are not allowed to delete customers.

        Args:
            request (Request): The request object for the delete operation.

        Returns:
            Response: A response indicating the result of the delete attempt, including success or error details.
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
