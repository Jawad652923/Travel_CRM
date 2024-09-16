from django.urls import path
from .views.tokens import CustomTokenObtainView,CustomTokenRefreshView,CustomTokenVerifyView
from .views.add_sales_agent import SalesAgentCreateView

urlpatterns = [
    path('auth/token/',CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/',CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/',CustomTokenVerifyView.as_view(), name='token_verify'),
    path('sales-agent/',SalesAgentCreateView.as_view(), name='create_sales_agent'),
]
