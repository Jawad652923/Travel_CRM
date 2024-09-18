from django.db import models
from django.conf import settings
from customer.models import Customer
from services.models import Service

class Inquiries(models.Model):
    """
    Represents an inquiry made by a customer for services.

    Attributes:
        STATUS_CHOICES (list): A list of tuples representing the possible statuses for an inquiry.
        details (TextField): A detailed description of the inquiry.
        status (CharField): The current status of the inquiry, chosen from STATUS_CHOICES. Defaults to 'Open'.
        customer (ForeignKey): A foreign key linking to the Customer model, representing the customer who made the inquiry.
        assigned_sales_agent (ForeignKey): A foreign key linking to the user model, representing the sales agent assigned to the inquiry.
        services (ManyToManyField): A many-to-many relationship linking to the Service model, representing the services related to the inquiry.

    Methods:
        __str__(): Returns a string representation of the inquiry, including its ID and status.
    """
    STATUS_CHOICES =[
        ('Open','open'),
        ('In Progress','in progress'),
        ('Closed','closed'),
        
    ]
    details = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Open')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    assigned_sales_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service,related_name='inquiries')
    
    def __str__(self):
        """
        Return the string representation of the inquiry status.

        Returns:
            str: Status and ID of the inquiry.
        """
        return f'Inquiry{self.id} - {self.status}'