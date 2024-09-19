import logging
from rest_framework import generics
from ..serializers import SalesAgentSerializer
from ..utils import custom_response
from accounts.permissions import IsAdmin

logger = logging.getLogger(__name__)
class SalesAgentCreateView(generics.CreateAPIView):
    """
    API view to create a new user with optional role specification.

    This view handles the creation of new users and requires admin permissions.
    The endpoint expects a POST request with user details and will return a success
    message if the user is created successfully.

    Serializer:
        - SalesAgentSerializer: The serializer used to validate and save the user data.

    Permission Classes:
        - IsAdmin: Ensures that only admin users can access this endpoint.

    Methods:
        - post(request, *args, **kwargs): Handles the POST request to create
          a new user.
    """
    serializer_class = SalesAgentSerializer
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new user.

        Args:
            request (HttpRequest): The HTTP request object containing user data.

        Returns:
            Response: A DRF Response object with the result of the operation.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return custom_response(
                    status_code=201,
                    message="User created successfully.",
                    data=serializer.data
                )
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}")
                return custom_response(
                    status_code=500,
                    message="An error occurred while creating the user.",
                    data=None
                )
        else:
            logger.error(f"Validation error: {serializer.errors}")
            return custom_response(
                status_code=400,
                message="Invalid data.",
                data=serializer.errors
            )
