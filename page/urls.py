from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('home', views.home, name='home_page'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
 
    




]