from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class CustomTokenObtainView(TokenObtainPairView):
    """
    Custom view to handle JWT tokens with a standardized response format.

    This view extends the default TokenObtainPairView to return custom success or error 
    messages along with the access and refresh token.
    """

    def post(self,request,*args, **kwargs):
        """
        Handles POST requests to generate the JWT access and refresh token.

        Returns a custom response with the status, code, message, timestamp,access and 
        refresh token if the credentials are valid. Returns an error response 
        if the credentials are invalid.
        """
        response = super().post(request,*args,**kwargs)
        if response.status_code==200:
            return Response({
                "status":"Success",
                "code":response.status_code,
                "message":"token Created successfully",
                "timestamp":timezone.now(),
                "data":{
                    "access":response.data['access'],
                    "refresh":response.data['refresh'],
                }
            },status=status.HTTP_200_OK)

        else:
            return Response({
                "status":"error",
                "code":response.status_code,
                "message":"Invalid Credentials",
                "timestamp":timezone.now(), 
                "data":None
            },status=response.status_code)
            
            
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to handle JWT token refreshes with a standardized response format.

    This view extends the default TokenRefreshView to return custom success or error 
    messages along with the access token when refreshing tokens.
    """

    def post(self,request,*args, **kwargs):
        """
        Handles POST requests to refresh the JWT access token.

        Returns a custom response with the status, code, message, timestamp, and 
        new access token if the refresh is successful. Returns an error response 
        if the refresh fails.
        """
        response = super().post(request,*args,**kwargs)
        if response.status_code==200:
            return Response({
                "status":"Success",
                "code":response.status_code,
                "message":"token Refreshed successfully",
                "timestamp":timezone.now(),
                "data":{
                    "access":response.data['access'],
                }
            },status=status.HTTP_200_OK)

        else:
            return Response({
                "status":"error",
                "code":response.status_code,
                "message":"Token Refreshed Failed",
                "timestamp":timezone.now(), 
                "data":None
            },status=response.status_code)
            

class CustomTokenVerifyView(TokenVerifyView):
    """
    Custom view to verify JWT token with a standardized response format.

    This view extends the default TokenVerifyView to return custom success or error 
    messages.
    """

    def post(self,request,*args, **kwargs):
        """
        Handles POST requests to verify the JWT access token.

        Returns a custom response with the status, code, message and timestamp if the token is valid. Returns an error response 
        if the token is expired or invalid.
        """
        response = super().post(request,*args,**kwargs)
        if response.status_code==200:
            return Response({
                "status":"Success",
                "code":response.status_code,
                "message":"Token is valid",
                "timestamp":timezone.now(),
                "data":None
            },status=status.HTTP_200_OK)

        else:
            return Response({
                "status":"error",
                "code":response.status_code,
                "message":"Token Refreshed Failed",
                "timestamp":timezone.now(), 
                "data":None
            },status=response.status_code)            
            