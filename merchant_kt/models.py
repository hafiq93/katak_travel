from django.db import models
from user_kt.models import User  

# Create your models here.
class ListMerchantModule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True, null=True)  # E.g., "module_users", "module_reports"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)  # Name of the company
    department = models.CharField(max_length=255,blank=True, null=True)  # Name of the company
    address = models.TextField(blank=True, null=True)  # Company address
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Company phone number
    email = models.EmailField(blank=True, null=True)  # Company email
    website = models.URLField(blank=True, null=True)  # Company website URL
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies",blank=True, null=True)  # Link to User model
    
    def __str__(self):
        return self.name