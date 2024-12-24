from django.db import models
from user_kt.models import User
from django.core.validators import RegexValidator
# ///////////////////main page ///////////////////////////////////////
class MainPage(models.Model):
    intro = models.TextField()
    page = models.TextField(null=True)

    def __str__(self):
        return self.intro

class MainChoose(models.Model):
    main = models.TextField()
    description = models.TextField()
    page = models.TextField(null=True)


    def __str__(self):
        return self.main

class AboutUs(models.Model):
    intro = models.TextField()
    objective = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    page = models.TextField(null=True)


    def __str__(self):
        return self.intro 

class ContactUs(models.Model):
    email = models.EmailField(max_length=250)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
    )
    phone_2 = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
        blank=True,  # Optional field
        null=True
    )
    page = models.TextField(null=True)


    def __str__(self):
        return self.email

# /////////////////////////////////////////////////////////////////////////////////////////////////

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    tags = models.CharField(max_length=200, blank=True)  # Comma-separated tags
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()  # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"

class Rating(models.Model):
    destination = models.OneToOneField(Destination, on_delete=models.CASCADE, related_name="rating")
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)