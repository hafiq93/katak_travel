from django.db import models
from user_kt.models import User
from package_kt.models import System,Package,SubPackage,SubPackage_2

# Create your models here.
# /////////////////////////////////roles database/////////////////////////////////////////////////
# Roles
class Roles(models.Model):
    role_name = models.CharField(max_length=255)
    no_siri = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.role_name

class ListModule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True, null=True)  # E.g., "module_users", "module_reports"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    permission_name = models.CharField(max_length=100, unique=True)
    no_siri = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, default="")  # Allow blank and set default to empty string
    code = models.CharField(max_length=100, unique=True,null=True)  # E.g., "can_add_user"
    module = models.ForeignKey(ListModule, on_delete=models.CASCADE, null=True , related_name="permissions")

    def __str__(self):
        return f"{self.permission_name} ({self.module.name})"

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name="role_users")

    def __str__(self):
        return f"{self.user.email} - {self.role.role_name}"

class RolePackage(models.Model):  # Modified RolePermission to RolePackage
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name="role_packages")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="package_roles")

    def __str__(self):
        return f"{self.role.role_name} - {self.package.name}"

# ////////////////////////////////////////////Hotel database////////////////////////////////////////////////////////////////

class HotelStatus(models.Model):
    status = models.CharField(max_length=100)  

    def __str__(self):
        return self.status

# HotelType Model
class HotelType(models.Model):
    type_name = models.CharField(max_length=100)  # Example: 'Hotel', 'Apartments', 'Villas'

    def __str__(self):
        return self.type_name

class HotelFacilities(models.Model):
    type_name = models.CharField(max_length=100)  # Example: ,'pool,'parking'
    icon_main = models.CharField(max_length=100, null=True, blank=True)  # Icon class (e.g., FontAwesome)

    def __str__(self):
        return self.type_name

# use for type of room
class HotelRoom(models.Model): 
    type_name = models.CharField(max_length=100)  # Example: 'Studio', 'Standard', 'Queen'
    description = models.TextField(null=True, blank=True)  # New description field
    
   
    def __str__(self):
        return self.type_name

# facilites in hotel 
class RoomFacilities(models.Model):
    type_name = models.CharField(max_length=100)  # 'wifi.private pool,bathtub'
    icon_main = models.CharField(max_length=100, null=True, blank=True)  # Icon class (e.g., FontAwesome)


    def __str__(self):
        return self.type_name

# use for view from room
class RoomView(models.Model):
    type_name = models.CharField(max_length=100)  

    def __str__(self):
        return self.type_name

# use for bed room
class RoomBed(models.Model):
    type_name = models.CharField(max_length=100) 

    def __str__(self):
        return self.type_name

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.country}"
# ////////////////////////////////////////////////////////////////////////////////
class MerchantList(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50, unique=True)
    register_no = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return self.name


class MainMerchant(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MerchantType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon_class = models.CharField(max_length=100, blank=True, null=True)
    main_category = models.ForeignKey(MainMerchant, on_delete=models.CASCADE, related_name='merchant_types', blank=True, null=True)

    def __str__(self):
        return self.name
        
# combine between merchant list and main merchant
class MerchantCategory(models.Model):
    merchant_list = models.ForeignKey(
        MerchantList,
        on_delete=models.CASCADE,
        related_name='merchant_categories',  # Changed related_name to avoid conflicts
        blank=True,
        null=True
    )
    main_category = models.ForeignKey(
        MainMerchant,
        on_delete=models.CASCADE,
        related_name='merchant_categories',  # Changed related_name to avoid conflicts
        blank=True,
        null=True
    )

    def __str__(self):
        # Added a __str__ method to display meaningful information.
        return f"{self.merchant_list} - {self.main_category}"


class MerchantLogin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Increased length for better security
    
    def __str__(self):
        return self.username  # Fixed self.name to self.username