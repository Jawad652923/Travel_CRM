from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer
from accounts.permissions import IsAdminOrSalesAgent
from .utils import custom_response

class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing service data.

    This viewset provides CRUD operations for `Service` instances. 
    Both admins and sales agents have full access to create, retrieve, update, and delete services.

    Attributes:
        serializer_class (ServiceSerializer): The serializer class used for service data.
        permission_classes (list): The list of permissions classes applied to this viewset.
        queryset (QuerySet): The queryset of `Service` instances.

    Methods:
        get_queryset():Returns a queryset of services based on user role. Admins have access to all services, while sales agents can access all services.
        list(request, *args, **kwargs): Retrieves a list of all services accessible by the user.
        retrieve(request, *args, **kwargs): Retrieves a specific service by ID.
        create(request, *args, **kwargs): Creates a new service with the provided data.
        update(request, *args, **kwargs): Updates an existing service with the provided data.
        destroy(request, *args, **kwargs): Deletes a service by ID.
    """
    
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrSalesAgent]
    queryset = Service.objects.all()
    
    def get_queryset(self):
        """
        Returns a queryset of services based on user role.
        Admins have access to all services, while sales agents have access to all services.
        """
        user = self.request.user
        if user.role == 'admin' or user.role == 'sales_agent':
            return Service.objects.all()
        return Service.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of services.

        Returns:
            Response: A response object containing the list of services or a message indicating no services found.
        """
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            response_data = custom_response(
                status_code=200,
                message="Services retrieved successfully.",
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = custom_response(
                status_code=404,
                message='No services found.',
                data=[]
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific service by ID.

        Returns:
            Response: A response object containing the service data or a message indicating service not found.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Service not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        response_data = custom_response(
            status_code=200,
            message="Service retrieved successfully.",
            data=serializer.data
        )
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a new service with the provided data.

        Returns:
            Response: A response object containing the created service data or a message indicating invalid fields.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = custom_response(
                status_code=201,
                message="Service created successfully.",
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
        Update an existing service with the provided data.

        Returns:
            Response: A response object containing the updated service data or a message indicating invalid data.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Service not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = custom_response(
                status_code=200,
                message="Service updated successfully.",
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
        Delete a service by ID.

        Returns:
            Response: A response object indicating successful deletion or a message indicating service not found.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Service not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(instance)
        response_data = custom_response(
                status_code=200,
                message="Service successfully deleted.",
                data=None
            )
        return Response(response_data, status=status.HTTP_200_OK)
