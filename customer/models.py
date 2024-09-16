from django.db import models
from accounts.models import CustomUser

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    
    assigned_sales_agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="customers")
    def __str__(self) :
        return self.name