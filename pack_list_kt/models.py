# D:\Work\katak_travel\pack_list_kt\models.py
from django.db import models
from admin_kt.models import Location
from user_kt.models import User
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from admin_kt.models import MainMerchant, MerchantType
import random
import string
from django_countries.fields import CountryField  # Optional for country selection

class Location(models.Model):
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.country}"

class MerchantPackage(models.Model):
    merchant = models.CharField(max_length=100)  # You could replace this with a ForeignKey if merchants are stored in a separate table
    
    # Address fields
    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.ForeignKey('Location', related_name="merchant_packages", on_delete=models.CASCADE, null=True, blank=True)

    # Contact details
    contact_person = models.CharField(max_length=50, null=True, blank=True)  # Renamed from 'pic'
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.merchant



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

    user_pic = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    
    # Minimum and Maximum Pax
    min_pax = models.PositiveIntegerField(default=1,blank=True, null=True)
    max_pax = models.PositiveIntegerField(blank=True, null=True)
    

    person = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    info = models.TextField(blank=True, null=True)
    date_of_travel = models.TextField(blank=True, null=True)

    # Duration fields
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    code = models.CharField(max_length=50, blank=True, null=True)

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

class PackageMerchant(models.Model):
    package = models.ForeignKey('Package', related_name="package_merchants", on_delete=models.CASCADE)
    merchant_list = models.ForeignKey(MerchantPackage, on_delete=models.CASCADE, related_name='package_merchants', blank=True, null=True)
    merchant_type = models.ForeignKey(MerchantType, on_delete=models.CASCADE, related_name="package_merchants", blank=True, null=True)
    name = models.CharField(max_length=100)
    merchant_code = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Merchant code field

    def generate_merchant_code(self):
        # Generate a random string of 8 characters (you can change the length)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def save(self, *args, **kwargs):
        # If merchant_code is not provided, generate a new one
        if not self.merchant_code:
            self.merchant_code = self.generate_merchant_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductDetails(models.Model):
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/')  # Files will be uploaded to 'media/product_images/'
    package_merchant = models.ForeignKey(
        'PackageMerchant', 
        on_delete=models.CASCADE, 
        related_name='product_details'
    )  # ForeignKey to PackageMerchant

    def __str__(self):
        return self.product_name


class PackageItem(models.Model):
    merchant_list = models.ForeignKey(
        PackageMerchant, on_delete=models.CASCADE, related_name='pack_price', blank=True, null=True
    )
    name = models.CharField(max_length=100)
    merchant_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def commission_amount(self):
        return (self.selling_price - self.merchant_price) * (self.commission_percent / 100)

    def __str__(self):
        return self.name

