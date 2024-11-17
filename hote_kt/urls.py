from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('hotel/main', views.hotel_main, name='main_hotel'),
   
]