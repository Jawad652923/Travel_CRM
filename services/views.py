from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer
from accounts.permissions import IsAdminOrSalesAgent
from .utils import custom_response

class ServiceViewSet(viewsets.ModelViewSet):
    """
    ServiceViewSet to manage service data.
    Both admins and sales agents have full CRUD access.
    """    
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrSalesAgent]
    queryset = Service.objects.all()
    
    def get_queryset(self):
        """
        Admins can access all services. Sales agents can access services linked to customers assigned to them through inquiries.
        """
        user = self.request.user
        if user.role == 'admin' or user.role == 'sales_agent':
            return Service.objects.all()
        return Service.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of services.
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
        Retrieve a specific service.
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
        Allow sales agents and admins to create a new service.
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
        Allow sales agents and admins to update a service.
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
        Allow both sales agents and admins to delete a service.
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
