from django.contrib.auth.models import BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Create Custome user manager for custom user model to create user and super_user .
    """
    def create_user(self,username,email,password=None,**extra_fields):
        if not username:
            raise ValueError("The Username must be set.")
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username,email,password,**extra_fields)