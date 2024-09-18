from django.db import models
from accounts.models import CustomUser

class Customer(models.Model):
    """
    Represents a customer in the system.

    Attributes:
        name (str): The full name of the customer.
        email (str): The email address of the customer, must be unique.
        phone_no (str): The phone number of the customer.
        address (str): The residential address of the customer.
        assigned_sales_agent (ForeignKey): The sales agent assigned to this customer, linked to the CustomUser model. This field is optional.

    Methods:
        __str__(): Returns the string representation of the customer, which is their name.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    assigned_sales_agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="customers")
    
    def __str__(self) :
        """
        Return the string representation of the customer.

        Returns:
            str: The name of the customer.
        """
        return self.name