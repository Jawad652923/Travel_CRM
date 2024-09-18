from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=15, null=True, blank=True, default=None) 

    def __str__(self):
        return self.name
