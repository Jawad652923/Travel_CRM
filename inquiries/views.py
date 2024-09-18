from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Inquiries
from .serializers import InquirySerializer
from accounts.permissions import IsAdminOrSalesAgent
from .utils import custom_response  

class InquiryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Inquiry data.

    This viewset provides actions to list, retrieve, create, update, partially update, and delete inquiries.
    - Admins have full access to all inquiries.
    - Sales agents can only view and update inquiries they are assigned to.
    - Sales agents cannot delete inquiries.

    Attributes:
        serializer_class (InquirySerializer): The serializer class used for converting Inquiry instances to and from JSON.
        permission_classes (list): List of permission classes used to restrict access to the viewset's actions.
        queryset (QuerySet): The base queryset for the viewset.

    Methods:
        get_queryset(): Returns the queryset based on the user's role. Admins see all inquiries, sales agents see only their assigned inquiries.
        list(request, *args, **kwargs): Retrieve a list of inquiries, either all or filtered based on the user's role.
        retrieve(request, *args, **kwargs): Retrieve a specific inquiry, with access control based on the user's role.
        create(request, *args, **kwargs): Create a new inquiry. Sales agents are assigned as the creator.
        update(request, *args, **kwargs): Update an existing inquiry. Admins can update any inquiry; sales agents can only update their assigned inquiries.
        partial_update(request, *args, **kwargs): Partially update an existing inquiry.
        destroy(request, *args, **kwargs): Delete an inquiry. Admins have full delete permissions; sales agents cannot delete inquiries.
    """
    serializer_class = InquirySerializer
    permission_classes = [IsAdminOrSalesAgent]
    queryset = Inquiries.objects.all()

    def get_queryset(self):
        """
        Returns the queryset of inquiries based on the user's role.

        Admins can view all inquiries. Sales agents can only view inquiries assigned to them.

        Returns:
            QuerySet: The filtered queryset of inquiries.
        """        
        user = self.request.user
        if user.role == 'admin':
            return Inquiries.objects.all()
        elif user.role == 'sales_agent':
            return Inquiries.objects.filter(assigned_sales_agent=user)
        return Inquiries.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of inquiries.

        Retrieves and returns a list of inquiries based on the user's role.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the list of inquiries or an appropriate message.
        """
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            response_data = custom_response(
                status_code=200,
                message="Inquiries retrieved successfully.",
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = custom_response(
                status_code=200,
                message='No inquiries found.',
                data=[]
            )
            return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific inquiry.

        Retrieves and returns the details of a specific inquiry based on the user's role.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the inquiry details or an error message.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Inquiry not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        
        serializer = self.get_serializer(instance)
        response_data = custom_response(
            status_code=200,
            message="Inquiry retrieved successfully.",
            data=serializer.data
        )
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Save the inquiry with the assigned_sales_agent field set.
        """
        user = self.request.user
        serializer.save(assigned_sales_agent=user)

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new inquiry.

        Handles the creation of a new inquiry, assigning the current user as the sales agent if applicable.

        Args:
            request (Request): The HTTP request object containing the data for the new inquiry.

        Returns:
            Response: The HTTP response object containing the created inquiry data or an error message.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = custom_response(
                status_code=201,
                message="Inquiry created successfully.",
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
        Update an existing inquiry.

        Updates the details of an existing inquiry based on the provided data.

        Args:
            request (Request): The HTTP request object containing the updated data for the inquiry.

        Returns:
            Response: The HTTP response object containing the updated inquiry data or an error message.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Inquiry not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = custom_response(
                status_code=200,
                message="Inquiry updated successfully.",
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
        Partially update an existing inquiry.

        Partially updates the details of an existing inquiry based on the provided data.

        Args:
            request (Request): The HTTP request object containing the partial data for the inquiry.

        Returns:
            Response: The HTTP response object containing the partially updated inquiry data or an error message.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Inquiry not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        partial = True
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = custom_response(
                status_code=200,
                message="Inquiry updated successfully.",
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
        Delete an inquiry.

        Admins can delete any inquiry. Sales agents cannot delete inquiries.
        
        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object confirming the deletion or an error message.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Inquiry not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        user = self.request.user
        if user.role != 'admin':
            response_data = custom_response(
                status_code=403,
                message='You are not authorized to delete this inquiry.',
                data=None
            )
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        response_data = custom_response(
            status_code=200,
            message="Inquiry successfully deleted.",
            data=None
        )            
        return Response(response_data, status=status.HTTP_200_OK)
