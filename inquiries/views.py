from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Inquiries
from .serializers import InquirySerializer
from accounts.permissions import IsAdminOrSalesAgent
from .utils import custom_response  

class InquiryViewSet(viewsets.ModelViewSet):
    """
    InquiryViewSet to manage inquiry data. 
    Admins have full access, while sales agents can only view/update inquiries they are assigned to.
    """    
    serializer_class = InquirySerializer
    permission_classes = [IsAdminOrSalesAgent]
    queryset = Inquiries.objects.all()

    def get_queryset(self):
        """
        Admins can access all inquiries. Sales agents can only access inquiries they are assigned to.
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
        if user.role == 'sales_agent' and instance.assigned_sales_agent != user:
            response_data = custom_response(
                status_code=403,
                message='You are not authorized to access this inquiry.',
                data=None
            )
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
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
        Update an inquiry. Admins can update any inquiry, while sales agents can only update inquiries they are assigned to.
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
        Partially update an inquiry.
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
        Both admin and sales agent  can delete a inquiries.
        
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
        instance.delete()
        response_data = custom_response(
            status_code=200,
            message="Inquiry successfully deleted.",
            data=None
        )            
        return Response(response_data, status=status.HTTP_200_OK)
