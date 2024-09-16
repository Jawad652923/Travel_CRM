from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from django.db import models


class CustomUser(AbstractBaseUser,PermissionsMixin):
    """
    Used Django custom user model and for adding a 'role' field to define user roles
    such as 'admin' and 'sales_agent'.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('sales_agent', 'Sales Agent'),
    ]
    
    
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    