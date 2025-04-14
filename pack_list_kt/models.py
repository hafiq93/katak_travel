# D:\Work\katak_travel\pack_list_kt\models.py
from django.db import models
from admin_kt.models import Location
from user_kt.models import User
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from admin_kt.models import MainMerchant, MerchantType, Status, UserRole
import random
import string
from decimal import Decimal
# from django_countries.fields import CountryField  # Optional for country selection

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

# class Status(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     color = models.CharField(max_length=7, default="#FFFFFF")

#     def __str__(self):
#         return self.name

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

    pack_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

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

    def get_send_back_userroles(self, allowed_roles=None, base_userrole=None):
        from user.models import UserRole  # Local import avoids circular dependencies

        queryset = UserRole.objects.all().select_related('user', 'role')

        if allowed_roles:
            queryset = queryset.filter(role__in=allowed_roles)

        if base_userrole:
            queryset = queryset.filter(
                department=base_userrole.department,
                company=base_userrole.company
            )

        return queryset

    def __str__(self):
        return self.name

class PackageMerchant(models.Model):
    package = models.ForeignKey('Package', related_name="package_merchants", on_delete=models.CASCADE)
    merchant_list = models.ForeignKey(MerchantPackage, on_delete=models.CASCADE, related_name='package_merchants', blank=True, null=True)
    merchant_type = models.ForeignKey(MerchantType, on_delete=models.CASCADE, related_name="package_merchants", blank=True, null=True)
    # name = models.CharField(max_length=100)
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
        return f"Merchant Code: {self.merchant_code}"

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



class ProductItemTotal(models.Model):
    merchant = models.ForeignKey(
        PackageMerchant, on_delete=models.CASCADE, related_name='product_totals',blank=True, null=True
    )
    total_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"Total for Merchant {self.merchant.id} - Total Selling Price: ${self.total_selling_price:.2f}"


class PackageItemTotalLink(models.Model):
    package_item = models.ForeignKey(
        'PackageItem', on_delete=models.CASCADE, related_name='item_totals',blank=True, null=True
    )
    product_item_total = models.ForeignKey(
        'ProductItemTotal', on_delete=models.CASCADE, related_name='package_items',blank=True, null=True
    )
    
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Link between {self.package_item} and {self.product_item_total}"



class PackageItem(models.Model):
    merchant_list = models.ForeignKey(
        PackageMerchant, on_delete=models.CASCADE, related_name='pack_item', blank=True, null=True
    )
    product_details = models.ForeignKey(
        ProductDetails, on_delete=models.CASCADE, related_name='pack_item', blank=True, null=True
    )

    # Price Details
    adult_selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    adult_agent_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    adult_commission_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    adult_commission_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    adult_number = models.PositiveIntegerField(default=0)
    
    children_selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    children_agent_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    children_commission_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    children_commission_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    children_number = models.PositiveIntegerField(default=0)
    
    # Summary and Total Price Calculation
    total_adult_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_children_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grand_total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensure that all price fields are not None, and replace None with Decimal('0.00')
        self.adult_selling_price = self.adult_selling_price if self.adult_selling_price is not None else Decimal('0.00')
        self.adult_agent_price = self.adult_agent_price if self.adult_agent_price is not None else Decimal('0.00')
        self.children_selling_price = self.children_selling_price if self.children_selling_price is not None else Decimal('0.00')
        self.children_agent_price = self.children_agent_price if self.children_agent_price is not None else Decimal('0.00')

        # Now perform the calculations
        self.adult_commission_price = self.adult_selling_price - self.adult_agent_price
        self.adult_commission_percent = (self.adult_commission_price / self.adult_selling_price) * 100 if self.adult_selling_price else 0
        self.total_adult_price = self.adult_selling_price * self.adult_number
        
        self.children_commission_price = self.children_selling_price - self.children_agent_price
        self.children_commission_percent = (self.children_commission_price / self.children_selling_price) * 100 if self.children_selling_price else 0
        self.total_children_price = self.children_selling_price * self.children_number
        
        self.grand_total_price = self.total_adult_price + self.total_children_price
        super().save(*args, **kwargs)

        # **Ensure that PackageItem is linked to ProductItemTotal**
        self.link_to_product_item_total()

    def link_to_product_item_total(self):
        # Get the first ProductItemTotal or specify a filter to ensure only one
        product_total = ProductItemTotal.objects.first()  # Or use a filter to get the right one

        if product_total:  # Ensure that there's a valid ProductItemTotal
            # Check if the link already exists
            link_exists = PackageItemTotalLink.objects.filter(
                package_item=self, product_item_total=product_total
            ).exists()

            # If link does not exist, create it
            if not link_exists:
                PackageItemTotalLink.objects.create(
                    package_item=self,
                    product_item_total=product_total
                )

    def __str__(self):
        return self.product_details.product_name


class PackageLog(models.Model):
    package = models.ForeignKey(Package, related_name="status_history", on_delete=models.CASCADE)
    from_user_role = models.ForeignKey(
        UserRole, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_packages"
    )
    
    to_user_role = models.ForeignKey(
        UserRole, on_delete=models.SET_NULL, null=True, blank=True, related_name="received_packages"
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.package.name} | From: {self.from_user_role} → To: {self.to_user_role}"

    class Meta:
        ordering = ['-updated_at']
    
    def save(self, *args, **kwargs):
        # No need to store the role as it's linked through the UserRole model
        super().save(*args, **kwargs)


class PackCategory(models.Model):
    package = models.ForeignKey('Package', on_delete=models.CASCADE, related_name='pack_categories')
    merchant_type = models.ForeignKey(MerchantType, on_delete=models.CASCADE, related_name='pack_categories')

    class Meta:
        unique_together = ('package', 'merchant_type')

    def __str__(self):
        return f"{self.package.name} - {self.merchant_type.name}"