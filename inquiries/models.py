from django.db import models
from django.conf import settings
from customer.models import Customer
from services.models import Service

class Inquiries(models.Model):
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
        return f'Inquiry{self.id} - {self.status}'