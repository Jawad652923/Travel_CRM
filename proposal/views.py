from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Proposals
from .serializers import ProposalSerializer
from accounts.permissions import IsAdminOrSalesAgent
from .utils import custom_response  

class ProposalViewSet(viewsets.ModelViewSet):
    """
    ProposalViewSet to manage proposal data. 
    """    
    serializer_class = ProposalSerializer
    permission_classes = [IsAdminOrSalesAgent]
    queryset = Proposals.objects.all()

    def get_queryset(self):
        """
        Retrieve a queryset of proposals based on user role.
        
        Admins have full access, while sales agents can only access proposals related to their inquiries.
        
        Returns:
            QuerySet: A queryset of `Proposals` objects.
        """        
        user = self.request.user
        if user.role == 'admin':
            return Proposals.objects.all()
        elif user.role == 'sales_agent':
            return Proposals.objects.filter(inquiry__assigned_sales_agent=user)
        return Proposals.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of proposals.

        Admin can retrieve all proposals, while sales agents can only retrieve proposals they created.
        
        Args:
            request (Request): The request object.

        Returns:
            Response: A response containing a list of proposals or a message if no proposals are found.
        """
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            response_data = custom_response(
                status_code=200,
                message="Proposals retrieved successfully.",
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = custom_response(
                status_code=200,
                message='No proposals found.',
                data=[]
            )
            return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific proposal.

        Admin can view any proposal, while sales agents can only view proposals they created.

        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: A response containing the proposal data or an error message if the proposal is not found.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Proposal not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    
        serializer = self.get_serializer(instance)
        response_data = custom_response(
            status_code=200,
            message="Proposal retrieved successfully.",
            data=serializer.data
        )
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Save the proposal instance.

        Args:
            serializer (ProposalSerializer): The serializer instance with the validated data.

        Returns:
            None
        """
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new proposal.

        Args:
            request (Request): The request object containing proposal data.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: A response containing the created proposal data or an error message if validation fails.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = custom_response(
                status_code=201,
                message="Proposal created successfully.",
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
        Update an existing proposal.

        Admins can update any proposal, while sales agents can only update proposals related to their inquiries.

        Args:
            request (Request): The request object containing updated proposal data.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: A response containing the updated proposal data or an error message if validation fails.
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Proposal not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = custom_response(
                status_code=200,
                message="Proposal updated successfully.",
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
        Partially update an existing proposal.

        Args:
            request (Request): The request object containing partial updated proposal data.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: A response containing the partially updated proposal data or an error message if validation fails.
        """
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Proposal not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        partial = True
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = custom_response(
                status_code=200,
                message="Proposal updated successfully.",
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
        Delete a specific proposal.

        Both admin and sales agents can delete proposals related to their inquiries.

        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Keyword arguments.

        Returns:
            Response: A response confirming the proposal deletion or an error message if the proposal is not found.
        """        
        try:
            instance = self.get_object()
        except:
            response_data = custom_response(
                status_code=404,
                message='Proposal not found.',
                data=None
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        response_data = custom_response(
            status_code=200,
            message="Proposal successfully deleted.",
            data=None
        )            
        return Response(response_data, status=status.HTTP_200_OK)
