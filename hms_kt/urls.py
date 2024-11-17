from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('dashboard/', views.dashboard, name='hms-dashboard'),
    path('hotel/', views.hotel_list, name='hms-list'),
    path('register_hotel/', views.register_hotel, name='register_hotel'),  # For creating a new hotel
    path('register_hotel/<int:hotel_id>/1', views.register_hotel, name='register_hotel'),  # For editing an existing hotel
    path('register_hotel/<int:hotel_id>/2/', views.register_hotel_2, name='hms-register2'),
    path('register_hotel/<int:hotel_id>/3/', views.register_hotel_3, name='hms-register3'),
    path('delete_hotel_image/<int:image_id>/', views.delete_hotel_image, name='delete_hotel_image'),  # Add this line
    path('register_hotel/<int:hotel_id>/4/', views.register_hotel_4, name='hms-register4'),
]