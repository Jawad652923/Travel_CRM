from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin user full resource access. 
    """
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role =='admin'
    
class IsSalesAgent(BasePermission):
    """
    Custom permission to allow sales agent to create and manage inquiries, proposal, services and customer data.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales_agent'