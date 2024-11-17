from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField
import datetime 

# Create your models here.
GENDER = (
  
    ("Female","Female"),
    ("Male","Male"),

)

IDENTITY_TYPE = (
    ("Identication Number (I/C)","Identication Number (I/C)"),
    ("Passport Number","Passport Number"),

)

def user_directory_path(instance, filename):
    ext = filename.split(".")[-1] #name of image.jpg
    filename = "%s.%s" %(instance.user.id, filename) #name
    return "user_{0}/{1}".format(instance.user.id,filename) #user_1,


class User(AbstractUser):
    username = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)

    otp = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvwxyz1234567890") 
    image = models.FileField(upload_to=user_directory_path, default="default.jpg", null=True,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="")

    country = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=2000, null=True, blank=True)
    postcode = models.CharField(max_length=200, null=True, blank=True)

    identity_type = models.CharField(max_length=200, choices=IDENTITY_TYPE, null=True, blank=True)
    identity_no = models.CharField(max_length=500, null=True, blank=True)
    identity_image =  models.FileField(upload_to=user_directory_path, default="id.jpg", null=True,blank=True)

    facebook = models.URLField( null=True, blank=True)

    wallet = models.DecimalField(max_digits=12 , decimal_places=2, default=0.00)
    verified = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else f"{self.user.username}"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Only create the profile if it doesn't already exist
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)

post_save.connect(save_user_profile, sender=User)

    


    