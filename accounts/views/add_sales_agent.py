from rest_framework import generics
from ..serializers import SalesAgentSerializer
from ..utils import custom_response
from accounts.permissions import IsAdmin

class SalesAgentCreateView(generics.CreateAPIView):
    """
    A view to handle the post request to add or create sales_agent 
    this action only perform by admin only.
    """
    serializer_class = SalesAgentSerializer
    permission_classes = [IsAdmin]
    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return custom_response(
                status_code=201,
                message="Sales agent created successfully.",
                data=serializer.data
            )
        except Exception as e:
            return custom_response(
                status_code=401,
                message="You are not authorized to perform this action.",
                data=None
                )