from django.db import models
from inquiries.models import Inquiries
from services.models import Service

class Proposals(models.Model):
    """
    Model representing a proposal in response to an inquiry.

    Attributes:
        STATUS_CHOICES (list): A list of possible status choices for the proposal.
        inquiry (ForeignKey): The inquiry to which the proposal is related.
        details (TextField): Detailed description of the proposal.
        services (ManyToManyField): The services included in the proposal.
        status (CharField): Current status of the proposal, with choices including 'Pending', 'Accepted', and 'Rejected'.
        cost (DecimalField): The cost associated with the proposal.
    """
    STATUS_CHOICES=[
        ('Pending','pending'),
        ('Accepted','accepted'),
        ('Rejected','rejected'),
    ]
    
    inquiry = models.ForeignKey(Inquiries,on_delete=models.CASCADE,related_name='proposals')
    details = models.TextField()
    services = models.ManyToManyField(Service)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES)
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        """
        Return a string representation of the proposal.

        Returns:
            str: A string representing the proposal, including the inquiry ID.
        """
        return f'Proposal for Inquiry{self.inquiry.id}'