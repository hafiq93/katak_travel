# D:\Work\katak_travel\pack_list_kt\models.py
from django.db import models
from admin_kt.models import Location
from django.utils import timezone
from datetime import timedelta
from datetime import datetime

class Location(models.Model):
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.country}"

class PackageType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#FFFFFF")

    def __str__(self):
        return self.name

class Package(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True, null=True)  # New city field
    
    # Minimum and Maximum Pax
    min_pax = models.PositiveIntegerField(default=1,blank=True, null=True)
    max_pax = models.PositiveIntegerField(blank=True, null=True)

    person = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()

    # Duration fields
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    pack_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        # Ensure that start_date and end_date are datetime.date objects
        if isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, '%d/%m/%Y').date()

        if isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, '%d/%m/%Y').date()

        # Calculate duration in days
        if self.start_date and self.end_date:
            self.duration = (self.end_date - self.start_date).days

        # Auto-expire package
        if self.end_date and self.end_date < timezone.now().date():
            self.status = 'expired'
        else:
            self.status = 'active'

        # Validation for pax range
        if self.min_pax > self.max_pax:
            raise ValueError("Minimum Pax cannot be greater than Maximum Pax.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PackageItem(models.Model):
    package = models.ForeignKey(Package, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    merchant_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def commission_amount(self):
        return (self.selling_price - self.merchant_price) * (self.commission_percent / 100)

    def __str__(self):
        return self.name