from django.db import models
from admin_kt.models import UserRole,HotelType,HotelFacilities,HotelRoom,RoomFacilities,RoomView,RoomBed  # Import UserRole instead of User
from ckeditor.fields import RichTextField
import os

class ListHmsModule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True, null=True)  # E.g., "module_users", "module_reports"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

def hotel_image_upload_to(instance, filename):
    # Create a folder named after the hotel
    hotel_name = instance.hotel.hotel_name.replace(" ", "_")  # Replace spaces with underscores
    return os.path.join('hotel_images', hotel_name, filename)

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255)
    address = models.TextField()
    location = models.CharField(max_length=255)
    poscode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Associate the hotel with a UserRole
    registered_by_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name="hotels",null=True)

    def __str__(self):
        return self.hotel_name

    class Meta:
        ordering = ['hotel_name']

class SelectHotel(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="selected_hotels", null=True)
    description = RichTextField(blank=True)
    hotel_type = models.ForeignKey(HotelType, on_delete=models.CASCADE, related_name="selected_hotels", null=True)

    def __str__(self):
        return f"{self.hotel.hotel_name} - {self.hotel_type.type_name}"


class SelectFacilities(models.Model):
    select_hotel = models.ForeignKey(SelectHotel, on_delete=models.CASCADE, related_name="hotel_facilities")
    hotel_facility = models.ForeignKey(HotelFacilities, on_delete=models.CASCADE, related_name="select_facilities")

    def __str__(self):
        return f"{self.select_hotel.hotel.hotel_name} - {self.hotel_facility.type_name}"

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=hotel_image_upload_to)  # Use the custom upload function
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.hotel.hotel_name}"

class Hotel_Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_rooms")  # Link each room to a hotel
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name="hotel_room_instances")  # Link to HotelRoom model

    description = models.TextField(null=True, blank=True)  # Optional: use only if unique to each hotel-room combination

    def __str__(self):
        return f"{self.hotel.hotel_name} - {self.room.type_name}"


    