from django.urls import path
from .views import CustomTokenObtainView,CustomTokenRefreshView,CustomTokenVerifyView
urlpatterns = [
    path('token/',CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/',CustomTokenVerifyView.as_view(), name='token_verify'),
]
