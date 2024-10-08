from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin user full resource access. 
    """
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role =='admin'
    
class IsSalesAgent(BasePermission):
    """
    Custom permission to allow only sales agent to create and manage inquiries, proposal, services and customer data.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales_agent'
    
class IsAdminOrSalesAgent(BasePermission):
    """
    Permission class that grants full access to both Admin and Sales Agents to manage inquiries, proposal and services .
    """
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'sales_agent']