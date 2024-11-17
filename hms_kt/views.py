from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Hotel,SelectHotel,SelectFacilities,HotelImage
from admin_kt.models import UserRole,HotelType,HotelFacilities

# Create your views here.
def dashboard(request):
    return render(request, 'hms_kt/hms_dashboard.html')  # Add your template

# Create your views here.
def hotel_list(request):
    return render(request, 'hms_kt/hms_list.html')  # Add your template

@login_required 
def register_hotel(request, hotel_id=None):  # Accept an optional hotel_id parameter
    # Get the user's roles
    user_roles = UserRole.objects.filter(user=request.user)
    allowed_roles = ["Admin", "Superadmin", "Hotel Admin"]

    # Check if the user has one of the allowed roles
    if not user_roles.filter(role__role_name__in=allowed_roles).exists():
        messages.error(request, "You do not have permission to register a hotel.")
        return redirect("forbidden")  # Redirect to a forbidden page or error message

    hotel = None  # Initialize hotel variable for the context

    # Initialize form data variables
    hotel_name = ''
    address = ''
    location = ''
    poscode = ''
    city = ''
    region = ''
    country = ''
    description = ''

    if hotel_id:  # If an ID is provided, retrieve the hotel
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            hotel_name = hotel.hotel_name
            address = hotel.address
            location = hotel.location
            poscode = hotel.poscode
            city = hotel.city
            region = hotel.region
            country = hotel.country
            description = hotel.description
        except Hotel.DoesNotExist:
            messages.error(request, "Hotel not found.")
            return redirect("hotel_list")  # Redirect to a hotel list or error page

    if request.method == "POST":
        # Get the data from the form
        hotel_name = request.POST.get("hotel_name")
        address = request.POST.get("address")
        location = request.POST.get("location")
        poscode = request.POST.get("poscode")
        city = request.POST.get("city")
        region = request.POST.get("region")
        country = request.POST.get("country")
        description = request.POST.get("description", "")

        # Create or update the hotel instance
        if hotel:
            # Update the existing hotel
            hotel.hotel_name = hotel_name
            hotel.address = address
            hotel.location = location
            hotel.poscode = poscode
            hotel.city = city
            hotel.region = region
            hotel.country = country
            hotel.description = description
            hotel.save()
            messages.success(request, "Hotel updated successfully.")
        else:
            # Create a new hotel
            registered_by_role = user_roles.first()  # Choose the first role as the registered_by_role
            if registered_by_role:
                hotel = Hotel.objects.create(
                    hotel_name=hotel_name,
                    address=address,
                    location=location,
                    poscode=poscode,
                    city=city,
                    region=region,
                    country=country,
                    description=description,
                    registered_by_role=registered_by_role
                )
                messages.success(request, "Hotel registered successfully.")
                hotel_submitted = True  # Set flag to True after successful update
            else:
                messages.error(request, "Failed to register hotel: no valid user role found.")

    # Render the registration form along with the submitted hotel data
    return render(request, 'hms_kt/hms_addhotel.html', {
        'hotel': hotel,
        'hotel_name': hotel_name,
        'address': address,
        'location': location,
        'poscode': poscode,
        'city': city,
        'region': region,
        'country': country,
        'description': description,
    })

@login_required
def register_hotel_2(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel_types = HotelType.objects.all()
    facilities = HotelFacilities.objects.all()

    # Fetch or create `SelectHotel` entry for this hotel
    select_hotel, created = SelectHotel.objects.get_or_create(hotel=hotel)

    if request.method == "POST":
        description = request.POST.get('description')
        hotel_type_id = request.POST.get('hotel_type')
        selected_facilities = request.POST.getlist('hotel_facilities')

        # Update existing data
        select_hotel.description = description
        if hotel_type_id:
            select_hotel.hotel_type = HotelType.objects.get(id=hotel_type_id)
        select_hotel.save()

        # Update facilities by clearing existing and adding selected
        SelectFacilities.objects.filter(select_hotel=select_hotel).delete()  # Clear existing facilities
        for facility_id in selected_facilities:
            facility = HotelFacilities.objects.get(id=facility_id)
            SelectFacilities.objects.create(select_hotel=select_hotel, hotel_facility=facility)

        messages.success(request, "Hotel details updated successfully.")
        return redirect('hms-register2', hotel_id=hotel.id)  # Redirect back to the same page after submission

    return render(request, 'hms_kt/hms_addhotel_2.html', {
        'hotel': hotel,
        'hotel_types': hotel_types,
        'facilities': facilities,
        'selected_facilities': select_hotel.hotel_facilities.values_list('hotel_facility', flat=True),  # Pass selected facilities to the template
    })



def register_hotel_3(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":
        images = request.FILES.getlist('hotel_images')
        captions = request.POST.getlist('captions')  # Get captions list

        # Save each image with its corresponding caption
        for index, image in enumerate(images):
            caption = captions[index] if index < len(captions) else ""
            HotelImage.objects.create(hotel=hotel, image=image, caption=caption)

        messages.success(request, "Images uploaded successfully.")
        return redirect('hms-register3', hotel_id=hotel.id)  # Redirect to the same page to display updates

    # Fetch images for display
    all_images = hotel.images.all()  # Assuming "images" is the related name for images in Hotel model
    main_images = all_images[:4]  # First four images for main display
    detail_images = all_images[4:]  # Remaining images for detailed view

    return render(request, 'hms_kt/hms_addpicture.html', {
        'hotel': hotel,
        'main_images': main_images,
        'detail_images': detail_images,
    })

@login_required
def delete_hotel_image(request, image_id):
    image = get_object_or_404(HotelImage, id=image_id)
    hotel_id = image.hotel.id  # Get the hotel ID for redirecting
    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('hms-register3', hotel_id=hotel_id)

# Create your views here.
def register_hotel_4(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel_types = HotelType.objects.all()
    facilities = HotelFacilities.objects.all()

    return render(request, 'hms_kt/hms_selectroom.html', {
        'hotel': hotel,
        'hotel_types': hotel_types,
        'facilities': facilities,
        })  # Add your template
