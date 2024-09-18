from django.db import models

class Service(models.Model):
    """
    Represents a service offered in the system.

    Attributes:
        name (str): The name of the service.
        description (str): A detailed description of the service.
        price (str, optional): The price of the service. It can be null or blank, with a default value of None.

    Methods:
        __str__(): Returns the name of the service as its string representation.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=15, null=True, blank=True, default=None) 

    def __str__(self):
        return self.name
