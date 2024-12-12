from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from user_kt.models import User,Profile
from page.models import MainPage,MainChoose,AboutUs,ContactUs
from .models import Permission,Roles,UserRole, RolePermission,HotelType,HotelFacilities,HotelRoom,RoomFacilities,RoomBed,RoomView
import re
from django.db.models import Q # Import the User model from user_kt app

def admin_required(user):
    return user.is_superuser or user.is_staff

# ///////////////////////////////////////////////////////////////////////////////

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def dashboard(request):
    # Your dashboard view logic
    return render(request, 'admin_kt/dashboard.html')

# ////////////////////////////////////////////////////////////////////////////////////////

@user_passes_test(admin_required, login_url='/login/')
def main_page(request):
    main_pages = MainPage.objects.all()  # Fetch all MainPage entries
    main_choose = MainChoose.objects.all()  # Fetch all MainPage entries
    return render(request, 'admin_kt/page_main.html', {'main_pages': main_pages,'main_choose': main_choose})


@user_passes_test(admin_required, login_url='/login/')
def main_edit(request, id):
    main_page = get_object_or_404(MainPage, id=id)

    if request.method == 'POST':
        # Get data from the form
        intro = request.POST.get('intro')
        page = request.POST.get('page')

        # Update the model instance
        main_page.intro = intro
        main_page.page = page
        main_page.save()

        # Redirect back to the main page
        return redirect('main_page')

    return render(request, 'admin_kt/page_main_edit.html', {
        'main_page': main_page,
    })

@user_passes_test(admin_required, login_url='/login/')
def main_choose(request, id):
    main_choose = get_object_or_404(MainChoose, id=id)
    

    if request.method == 'POST':
        # Get data from the form
        main = request.POST.get('intro')
        description = request.POST.get('description')
        page = request.POST.get('page')

        # Update the model instance
        main_choose.main = main
        main_choose.description = description
        main_choose.page = page
        main_choose.save()

        # Redirect back to the same edit page
        return redirect('main_page')

    return render(request, 'admin_kt/page_choice.html', {
        'main_choose': main_choose,
    })

@user_passes_test(admin_required, login_url='/login/')
def main_about(request):
    main_about = AboutUs.objects.all()  # Fetch all MainPage entries
    main_contact = ContactUs.objects.all()  # Fetch all MainPage entries
    return render(request, 'admin_kt/page_about.html', {'main_about': main_about,'main_contact': main_contact})

# /////////////////////////////////////package//////////////////////////////////////////

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def package_list(request):
    # Your dashboard view logic
    return render(request, 'admin_kt/package_list.html')

# ////////////////////////////////////////////////////////////////////////////////////////



@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def user_list(request):
    query = request.GET.get('q')

    # Allow only alphanumeric characters and spaces in the query
    if query and not re.match(r'^[a-zA-Z0-9\s]*$', query):
        messages.error(request, 'Invalid characters in search query.')
        query = None  # Clear the query

    users = User.objects.select_related('profile').all()

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(profile__first_name__icontains=query) |
            Q(profile__last_name__icontains=query)
        )
    return render(request, 'admin_kt/user_list.html', {'users': users, 'query': query})


@user_passes_test(admin_required, login_url='/login/')
def user_profile(request, user_id):
    user = get_object_or_404(User.objects.select_related('profile'), id=user_id)
    return render(request, 'admin_kt/user_profile.html', {'user': user})


# /////////////////////////hote list////////////////////////////////////

@user_passes_test(admin_required, login_url='/login/')
def hotel_list(request):
    # Your dashboard view logic
    return render(request, 'admin_kt/hotel_list.html')

# ////////////////////////////hotel type/////////////////////////////////////////////
@user_passes_test(admin_required, login_url='/login/')
def hotel_type(request):
    # Your dashboard view logic
    hotel_type = HotelType.objects.all()
    return render(request, 'admin_kt/hotel_type.html',{'hotel_type': hotel_type})

@user_passes_test(admin_required, login_url='/login/')
def hotel_type_edit(request):
    if request.method == 'POST':
        hotel_type_id = request.POST.get('hotel_type_id')
        type_name = request.POST.get('type_name')

        # Fetch and update the hotel type
        hotel_type = get_object_or_404(HotelType, id=hotel_type_id)
        hotel_type.type_name = type_name
        hotel_type.save()

        # Redirect back to the hotel type list page (or wherever you want)
        return redirect('hotel_type')

@user_passes_test(admin_required, login_url='/login/')
def hotel_type_delete(request, hotel_type_id):
    hotel_type = get_object_or_404(HotelType, id=hotel_type_id)
    hotel_type.delete()
    return redirect('hotel_type')  # This should redirect correctly

@user_passes_test(admin_required, login_url='/login/')
def hotel_type_add(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        new_hotel_type = HotelType.objects.create(type_name=type_name)
        return redirect('hotel_type')  # Redirect to the list view

# ////////////////////hotel facilities///////////////////////////////////////////////////////////////
@user_passes_test(admin_required, login_url='/login/')
def hotel_facilities(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    if query:
        # Filter hotel facilities by type_name containing the search query
        hotel_facilities = HotelFacilities.objects.filter(
            Q(type_name__icontains=query) | Q(icon_main__icontains=query)
        )
    else:
        # If no search query, display all facilities
        hotel_facilities = HotelFacilities.objects.all()
    
    context = {
        'hotel_facilities': hotel_facilities,
        'query': query  # Pass the query to keep the search term in the input
    }
    return render(request, 'admin_kt/hotel_facilities.html', context)

@user_passes_test(admin_required, login_url='/login/')
def hotel_facility_add(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        icon_main = request.POST.get('icon_main')
        HotelFacilities.objects.create(type_name=type_name, icon_main=icon_main)
        return redirect('hotel_facilities')

    return render(request, 'admin_kt/hotel_facilities.html')

@user_passes_test(admin_required, login_url='/login/')
def hotel_facility_edit(request):
    if request.method == 'POST':
        facility_id = request.POST.get('facility_id')  # Get the facility ID
        type_name = request.POST.get('type_name')      # Get the facility name
        icon_main = request.POST.get('icon_main')      # Get the icon

        # Fetch and update the hotel facility
        facility = get_object_or_404(HotelFacilities, id=facility_id)
        facility.type_name = type_name
        facility.icon_main = icon_main
        facility.save()

        # Redirect back to the hotel facilities list page
        return redirect('hotel_facilities')

    return render(request, 'admin_kt/hotel_facilities.html')
    

@user_passes_test(admin_required, login_url='/login/')
def hotel_facility_delete(request, facility_id):
    facility = get_object_or_404(HotelFacilities, id=facility_id)
    facility.delete()
    return redirect('hotel_facilities')

# /////////////////////////////hotel room/////////////////////////////////////////////////
@user_passes_test(admin_required, login_url='/login/')
def hotel_room(request):
    room_type = HotelRoom.objects.all()
    return render(request, 'admin_kt/hotel_room.html',{'room_type': room_type})

@user_passes_test(admin_required, login_url='/login/')
def room_type_edit(request):
    if request.method == 'POST':
        room_type_id = request.POST.get('room_type_id')  # Get the room_type_id from the form data
        type_name = request.POST.get('type_name')
        
        # Debug output to check the received room_type_id
        print("Received room_type_id:", room_type_id) 
        
        # Fetch and update the hotel room type
        room_type = get_object_or_404(HotelRoom, id=room_type_id)
        room_type.type_name = type_name
        room_type.save()

        # Redirect to the list view after successful update
        return redirect('room_type')  # Replace 'room_type' with the actual name of your URL pattern
    
    # If not a POST request, return a 405 Method Not Allowed error
    return render(request, 'admin_kt/hotel_room.html')

@user_passes_test(admin_required, login_url='/login/')
def room_type_delete(request, room_type_id):
    room_type = get_object_or_404(HotelRoom, id=room_type_id)
    room_type.delete()
    return redirect('room_type')  # This should redirect correctly

@user_passes_test(admin_required, login_url='/login/')
def room_type_add(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        new_room_type = HotelRoom.objects.create(type_name=type_name)
        return redirect('room_type')  # Redirect to the list view after adding the room type
    else:
        # For GET request, render the add room type page/modal
        return render(request, 'admin_kt/hotel_room.html')  # Adjust the template path accordingly

# ////////////////////////////////room facilities/////////////////////////////////////////////
@user_passes_test(admin_required, login_url='/login/')
def hotel_room_faci(request):
    # Your dashboard view logic
    room_facilities = RoomFacilities.objects.all()
    return render(request, 'admin_kt/hotel_room_faci.html',{'room_facilities': room_facilities})

@user_passes_test(admin_required, login_url='/login/')
def room_facility_add(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        icon_main = request.POST.get('icon_main')
        RoomFacilities.objects.create(type_name=type_name, icon_main=icon_main)
        return redirect('hotel_room_faci')

    return render(request, 'admin_kt/hotel_room_faci.html')

@user_passes_test(admin_required, login_url='/login/')
def room_facility_edit(request):
    if request.method == 'POST':
        facility_id = request.POST.get('facility_id')  # Get the facility ID
        type_name = request.POST.get('type_name')      # Get the facility name
        icon_main = request.POST.get('icon_main')      # Get the icon

        # Fetch and update the hotel facility
        facility = get_object_or_404(RoomFacilities, id=facility_id)
        facility.type_name = type_name
        facility.icon_main = icon_main
        facility.save()

        # Redirect back to the hotel facilities list page
        return redirect('hotel_room_faci')

    return render(request, 'admin_kt/hotel_room_faci.html')
    

@user_passes_test(admin_required, login_url='/ login/')
def room_facility_delete(request, facility_id):
    facility = get_object_or_404(RoomFacilities, id=facility_id)
    facility.delete()
    return redirect('hotel_room_faci')

# ////////////////////////////////////hotel view//////////////////////////////////////

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def hotel_view(request):
    # Your dashboard view logic
    room_view = RoomView.objects.all()
    return render(request, 'admin_kt/hotel_view.html',{'room_view': room_view})

@user_passes_test(admin_required, login_url='/login/')
def view_add(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        RoomView.objects.create(type_name=type_name)
        return redirect('hotel_view')

    return render(request, 'admin_kt/hotel_view.html')

@user_passes_test(admin_required, login_url='/login/')
def view_edit(request):
    if request.method == 'POST':
        view_id = request.POST.get('view_id')  # Get the view ID from the form
        type_name = request.POST.get('type_name')  # Get the view name from the form

        # Fetch and update the RoomView object
        view = get_object_or_404(RoomView, id=view_id)
        view.type_name = type_name  # Update the name field with the new value
        view.save()

        # Redirect back to the hotel views list page
        return redirect('hotel_view')

    return render(request, 'admin_kt/hotel_view.html')


@user_passes_test(admin_required, login_url='/ login/')
def view_delete(request, view_id):
    view = get_object_or_404(RoomView, id=view_id)
    view.delete()
    return redirect('hotel_view')

#////////////////////////room bed////////////////////// 

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def room_bed(request):
    # Your dashboard view logic
    room_bed = RoomBed.objects.all()
    return render(request, 'admin_kt/hotel_bed.html',{'room_bed': room_bed})

@user_passes_test(admin_required, login_url='/login/')
def bed_add(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        RoomBed.objects.create(type_name=type_name)
        return redirect('room_bed')

    return render(request, 'admin_kt/hotel_bed.html')

@user_passes_test(admin_required, login_url='/login/')
def bed_edit(request):
    if request.method == 'POST':
        bed_id = request.POST.get('bed_id')  # Get the view ID from the form
        type_name = request.POST.get('type_name')  # Get the view name from the form

        # Fetch and update the RoomView object
        bed = get_object_or_404(RoomBed, id=bed_id)
        bed.type_name = type_name  # Update the name field with the new value
        bed.save()

        # Redirect back to the hotel views list page
        return redirect('room_bed')

    return render(request, 'admin_kt/hotel_bed.html')


@user_passes_test(admin_required, login_url='/ login/')
def bed_delete(request, bed_id):
    bed = get_object_or_404(RoomBed, id=bed_id)
    bed.delete()
    return redirect('room_bed')
# /////////////////////////////////////

@user_passes_test(admin_required, login_url='/login/')
def list_roles(request):
    roles = Roles.objects.all()
    # Your dashboard view logic
    return render(request, 'admin_kt/list_roles.html', {'roles': roles})

@user_passes_test(admin_required, login_url='/login/')
def list_permission(request):
    # Fetch all permissions
    permissions = Permission.objects.all()
    return render(request, 'admin_kt/list_permission.html', {'permissions': permissions})

@user_passes_test(admin_required, login_url='/login/')
def roles_permission(request):
    roles = Roles.objects.prefetch_related('role_permissions__permission').all()
    return render(request, 'admin_kt/user_roles_permission.html', {'roles': roles})

@user_passes_test(admin_required, login_url='/login/')
def edit_roles_permission(request):
    roles = Roles.objects.prefetch_related('role_permissions__permission').all()
    return render(request, 'admin_kt/user_edit_rnp.html', {'roles': roles})


@user_passes_test(admin_required, login_url='/login/')
def user_roles(request):
    # Fetch all users with their roles and permissions
    users = User.objects.prefetch_related('user_roles__role__role_permissions__permission')

    # Prepare data structure
    user_data = []
    for user in users:
        roles = user.user_roles.all()
        role_permissions = {
            role.role.role_name: [rp.permission.permission_name for rp in role.role.role_permissions.all()]
            for role in roles
        }
        user_data.append({
            'user': user,
            'roles_permissions': role_permissions,
        })

    context = {
        'user_data': user_data,
    }
    return render(request, 'admin_kt/user_roles.html', context)
# /////////////////////////////////////////////////////////////////////////////////////////////////////

@user_passes_test(admin_required, login_url='/login/')
def news(request):
   
    # Your dashboard view logic
    return render(request, 'admin_kt/news_news.html')

@user_passes_test(admin_required, login_url='/login/')
def review(request):
   
    # Your dashboard view logic
    return render(request, 'admin_kt/news_review.html')

@user_passes_test(admin_required, login_url='/login/')
def news_add(request):
   
    # Your dashboard view logic
    return render(request, 'admin_kt/news_add.html')