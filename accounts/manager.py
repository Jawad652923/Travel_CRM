from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for creating users and superusers.
    """
    def create_user(self, username, email, role, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set.")
        if not email:
            raise ValueError("The Email must be set.")
        if not role:
            raise ValueError("The Role must be set.")
        
        email = self.normalize_email(email)
        extra_fields.setdefault('role', role)  # Ensure role is set in extra_fields
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Set the role to 'admin'
        
        # Remove the role from extra_fields if it's already included
        return self.create_user(username, email, 'admin', password, **{k: v for k, v in extra_fields.items() if k != 'role'})
