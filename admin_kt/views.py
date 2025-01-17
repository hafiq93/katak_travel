from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from datetime import datetime,timedelta
from django.db.models import Count
from django.http import HttpResponse
from package_kt.models import System,Package,SubPackage,SubPackage_2
from user_kt.models import User,Profile
from analytics_kt.models import WebsiteAnalytics
from page.models import MainPage,MainChoose,AboutUs,ContactUs
from .models import Permission,Roles,UserRole, HotelType,HotelFacilities,HotelRoom,RoomFacilities,RoomBed,RoomView,RolePackage
import re
from django.db.models import Q # Import the User model from user_kt app
from django.core.paginator import Paginator
from django.http import JsonResponse
from collections import defaultdict
from pack_list_kt.models import Package
from django.contrib import messages

def admin_required(user):
    return user.is_superuser or user.is_staff

# ///////////////////////////////////////////////////////////////////////////////

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def dashboard(request):
    # Filter for URLs that contain either 'kataktravel.com' or 'www.kataktravel.com'
    analytics_data = WebsiteAnalytics.objects.filter(
        page_url__icontains='kataktravel.com'
    ).filter(
        page_url__icontains='www.kataktravel.com'
    ).order_by('-timestamp')
    
    total_visits = analytics_data.count()  # Count the visits for the filtered pages

    # Your dashboard view logic
    return render(request, 'admin_kt/dashboard.html', {'data': analytics_data, 'total_visits': total_visits})

# ////////////////////////////////////////////////////////////////////////////////////////
@login_required(login_url='/login/')
@user_passes_test(admin_required, login_url='/login/')
def main_page(request):
    main_pages = MainPage.objects.all()  # Fetch all MainPage entries
    main_choose = MainChoose.objects.all()  # Fetch all MainPage entries
    return render(request, 'admin_kt/page_main.html', {'main_pages': main_pages,'main_choose': main_choose})

@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
@user_passes_test(admin_required, login_url='/login/')
def main_about(request):
    main_about = AboutUs.objects.all()  # Fetch all MainPage entries
    main_contact = ContactUs.objects.all()  # Fetch all MainPage entries
    return render(request, 'admin_kt/page_about.html', {'main_about': main_about,'main_contact': main_contact})

# /////////////////////////////////////package//////////////////////////////////////////

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def package_dashboard(request):
    # Your dashboard view logic
    return render(request, 'admin_kt/package_dashboard.html')

@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def package_list(request):
    packages = Package.objects.all()  # Assuming you're fetching all packages
    return render(request, 'admin_kt/package_list.html', {'packages': packages})

def delete_package(request, id):
    package = get_object_or_404(Package, id=id)
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Package deleted successfully.')
        return redirect('package_list')  # Redirect to the package list page
    return redirect('package_list')

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

@login_required(login_url='/login/')
@user_passes_test(admin_required, login_url='/login/')
def user_profile(request, user_id):
    user = get_object_or_404(User.objects.select_related('profile'), id=user_id)
    return render(request, 'admin_kt/user_profile.html', {'user': user})


# /////////////////////////merchant & hotel dashboard////////////////////////////////////
@login_required(login_url='/login/')
@user_passes_test(admin_required, login_url='/login/')
def merhotel_dashboard(request):
    # Your dashboard view logic
    return render(request, 'admin_kt/merhotel_dashboard.html')

# /////////////////////////hote list////////////////////////////////////
@login_required(login_url='/login/')
@user_passes_test(admin_required, login_url='/login/')
def hotel_list(request):
    # Your dashboard view logic
    return render(request, 'admin_kt/hotel_list.html')

# ////////////////////////////hotel type/////////////////////////////////////////////
@login_required(login_url='/login/')
@user_passes_test(admin_required, login_url='/login/')
def hotel_type(request):
    # Your dashboard view logic
    hotel_type = HotelType.objects.all()
    return render(request, 'admin_kt/hotel_type.html',{'hotel_type': hotel_type})

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
@user_passes_test(admin_required, login_url='/login/')
def hotel_type_delete(request, hotel_type_id):
    hotel_type = get_object_or_404(HotelType, id=hotel_type_id)
    hotel_type.delete()
    return redirect('hotel_type')  # This should redirect correctly
    
@login_required(login_url='/login/')
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
    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        no_siri = request.POST.get('no_siri')  # Update if your field name differs
        # Validate input
        if not role_name:
            # Handle missing data error (optional)
            return render(request, 'admin_kt/list_roles.html', {'error': 'Role Name is required'})

        # Save to the database
        Roles.objects.create(role_name=role_name, no_siri=no_siri)

        # Redirect or reload page to prevent duplicate submissions
        return redirect('list_roles')

    roles = Roles.objects.all()
    return render(request, 'admin_kt/list_roles.html', {'roles': roles})

@user_passes_test(admin_required, login_url='/login/')
def edit_role(request):
    if request.method == 'POST':
        role_id = request.POST.get('id')
        role_name = request.POST.get('role_name')
        no_siri = request.POST.get('no_siri')

        # Fetch the role object
        role = get_object_or_404(Roles, id=role_id)

        # Update the role details
        role.role_name = role_name
        role.no_siri = no_siri
        role.save()

        # Redirect to the roles list
        return redirect('list_roles')

@user_passes_test(admin_required, login_url='/login/')
def delete_role(request, role_id):
    role = get_object_or_404(Roles, id=role_id)
    role.delete()  # Deletes the role object
    return redirect('list_roles')  # Redirects to the roles list page
    # /////////////////////////////////////////////////////////////
@user_passes_test(admin_required, login_url='/login/')
def list_permission(request):
    # Fetch all systems from the database
    systems = System.objects.all()

    # Get the active system based on the URL parameter or default to the first system
    active_tab = request.GET.get('active_tab', str(systems.first().id))

    # Get the system based on the active tab (system ID or name)
    current_system = System.objects.get(id=active_tab)

    # Fetch packages and subpackages for the current system
    permissions = []
    packages = Package.objects.filter(system=current_system)
    for idx, package in enumerate(packages, start=1):
        subpackages = SubPackage.objects.filter(package=package)

        # Build subpackage data with detail subpackages
        subpackage_data = []
        for subpackage in subpackages:
            detail_subpackages = SubPackage_2.objects.filter(subpackage=subpackage)
            subpackage_data.append({
                'name': subpackage.name,
                'details': [{'name': detail.name} for detail in detail_subpackages] if detail_subpackages.exists() else None
            })

        permissions.append({
            'number': f"{active_tab}.{idx}",  # Create hierarchical numbering
            'package': package.name,
            'subpackages': subpackage_data
        })

    context = {
        'systems': systems,  # Pass all systems to the template for tab selection
        'permissions': permissions,  # Permissions for the current system
        'active_tab': active_tab,  # Current active tab (system)
    }

    return render(request, 'admin_kt/list_permission.html', context)
# /////////////////////////////////////////////////////////////////////////////



@user_passes_test(admin_required, login_url='/login/')
def roles_permission(request):
    roles = Roles.objects.prefetch_related('role_packages__package').all()
    context = {
        'roles': roles
    }
    return render(request, 'admin_kt/user_roles_permission.html', context)

@user_passes_test(admin_required, login_url='/login/')
def edit_roles_permission(request, role_id):
    role = get_object_or_404(Roles, id=role_id)
    available_systems = System.objects.all()
    available_packages = Package.objects.all()
    assigned_packages = role.role_packages.all()

    if request.method == 'POST':
        if 'add_package' in request.POST:
            package_id = request.POST.get('package_id')
            package = get_object_or_404(Package, id=package_id)
            RolePackage.objects.get_or_create(role=role, package=package)

        if 'delete_package' in request.POST:
            package_id = request.POST.get('package_id')
            RolePackage.objects.filter(role=role, package_id=package_id).delete()

        return redirect('edit_roles_permission', role_id=role.id)

    context = {
        'role': role,
        'available_systems': available_systems,
        'available_packages': available_packages,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'admin_kt/user_edit_rnp.html', context)



def edit_roles_and_packages(request, role_id):
    # Get the role using the role_id from the URL
    role = get_object_or_404(Roles, id=role_id)

    if request.method == "POST":
        package_id = request.POST.get("package")
        action = request.POST.get("add_package")

        # Fetch the package using the ID
        package = get_object_or_404(Package, id=package_id)

        if action == "add_package":
            RolePackage.objects.create(role=role, package=package)
        elif action == "delete_package":
            RolePackage.objects.filter(role=role, package=package).delete()

    # Fetch data for dropdowns
    systems = System.objects.all()
    available_packages = Package.objects.all()

    # Group assigned packages by system
    assigned_packages_by_system = (
        RolePackage.objects.filter(role=role)
        .select_related("package__system")
        .order_by("package__system__name")
    )

    # Group packages by their system
    grouped_packages = {}
    for rp in assigned_packages_by_system:
        system_name = rp.package.system.name if rp.package.system else "No System"
        if system_name not in grouped_packages:
            grouped_packages[system_name] = []
        grouped_packages[system_name].append(rp)

    context = {
        "role": role,
        "available_systems": systems,
        "available_packages": available_packages,
        "grouped_packages": grouped_packages,
    }

    return render(request, "admin_kt/user_edit_rnp.html", context)

# API endpoint for dynamically populating dropdowns
def fetch_related_data(request):
    data_type = request.GET.get("type")
    parent_id = request.GET.get("id")
    
    if data_type == "packages":
        packages = Package.objects.filter(system_id=parent_id)
        data = [{"id": pkg.id, "name": pkg.name} for pkg in packages]
    elif data_type == "subpackages":
        subpackages = SubPackage.objects.filter(package_id=parent_id)
        data = [{"id": subpkg.id, "name": subpkg.name} for subpkg in subpackages]
    elif data_type == "subpackages_2":
        subpackages_2 = SubPackage_2.objects.filter(subpackage_id=parent_id)
        data = [{"id": subpkg2.id, "name": subpkg2.name} for subpkg2 in subpackages_2]
    else:
        data = []

    return JsonResponse({"data": data})
# //////////////////////////////////////////////////////////////////////////////////
@user_passes_test(admin_required, login_url='/login/')
def user_roles(request):
    users = User.objects.prefetch_related('user_roles__role__role_packages__package__system').all()
    roles = Roles.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user")
        role_id = request.POST.get("role")

        try:
            # Retrieve the user and role objects
            user = User.objects.get(id=user_id)
            role = Roles.objects.get(id=role_id)

            # Create or update the UserRole relationship
            UserRole.objects.get_or_create(user=user, role=role)

        except User.DoesNotExist:
            messages.error(request, "Selected user does not exist.")
        except Roles.DoesNotExist:
            messages.error(request, "Selected role does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        # Redirect to the same page to prevent resubmission
        return redirect("user_roles")

    user_data = []
    for user in users:
        roles_for_user = user.user_roles.all()
        roles_packages = []

        for role in roles_for_user:
            system_packages = {}
            for role_package in role.role.role_packages.all():
                system_name = role_package.package.system.name if role_package.package.system else "No System"
                if system_name not in system_packages:
                    system_packages[system_name] = []
                system_packages[system_name].append(role_package.package.name)

            roles_packages.append({
                'role_id': role.role.id,
                'role_name': role.role.role_name,
                'system_packages': system_packages,
            })

        user_data.append({
            'user': user,
            'roles_packages': roles_packages,
        })

    context = {
        'user_data': user_data,
        'users': users,
        'roles': roles,
    }
    return render(request, 'admin_kt/user_roles.html', context)




@user_passes_test(admin_required, login_url='/login/')
def user_roles_details(request, role_id, user_id):
    role = get_object_or_404(Roles, id=role_id)
    grouped_packages = {}

    # Group packages by their systems
    for role_package in role.role_packages.select_related('package', 'package__system').all():
        package = role_package.package
        system_name = package.system.name if package.system else "No System"

        # Fetch sub-packages and sub-package 2
        sub_packages = package.sub_packages.all()
        package_data = {
            "package_name": package.name,
            "sub_packages": [
                {
                    "name": sub_package.name,
                    "sub_packages_2": list(sub_package.sub_packages_2.all()),
                }
                for sub_package in sub_packages
            ],
        }

        if system_name not in grouped_packages:
            grouped_packages[system_name] = []
        grouped_packages[system_name].append(package_data)

    context = {
        'role': role,
        'grouped_packages': grouped_packages,
    }

    return render(request, 'admin_kt/user_role_details.html', context)




@user_passes_test(admin_required, login_url='/login/')
def get_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    roles = [role.role_name for role in user.user_roles.all()]  # Adjust based on your models
    return JsonResponse({
        'name': user.username,
        'email': user.email,
        'roles': roles,
    })
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



    # /////////////////////////////////////////////////////////////////////////////////////////////////////

@user_passes_test(admin_required, login_url='/login/')
def sales_dashboard(request):
   
    # Your dashboard view logic
    return render(request, 'admin_kt/sales_dashboard.html')


    # /////////////////////////////////////////////////////////////////////////////////////////////////////

@user_passes_test(admin_required, login_url='/login/')
def user_dashboard(request):
    # Get the current date and time
    current_time = now()
    start_date = current_time - timedelta(days=7)  # Default to last week

    # Check filter type
    filter_type = request.GET.get('filter', 'week')  # Default filter: 'week'
    if filter_type == 'day':
        start_date = current_time - timedelta(days=1)
    elif filter_type == 'month':
        start_date = current_time - timedelta(weeks=4)
    elif filter_type == 'year':
        start_date = current_time - timedelta(weeks=52)

    # Custom date range handling
    custom_start_date = request.GET.get('start_date')
    custom_end_date = request.GET.get('end_date')
    if custom_start_date and custom_end_date:
        try:
            start_date = datetime.strptime(custom_start_date, "%d-%m-%Y")
            end_date = datetime.strptime(custom_end_date, "%d-%m-%Y")
        except ValueError:
            end_date = current_time
    else:
        end_date = current_time

    # Corrected filter to handle URLs and date range properly
    analytics_data = WebsiteAnalytics.objects.filter(
        timestamp__range=(start_date, end_date),
        page_url__icontains='kataktravel.com'
    ).filter(
        Q(page_url__icontains='www.kataktravel.com') | Q(page_url__icontains='kataktravel.com')
    ).order_by('-timestamp')

    total_visits = analytics_data.count()

    # Group data for the chart
    grouped_data = analytics_data.values('timestamp__date').annotate(total_clicks=Count('id')).order_by('timestamp__date')
    

    # Prepare data for JavaScript
    labels = [data['timestamp__date'].strftime('%d-%m-%Y') for data in grouped_data]
    clicks = [data['total_clicks'] for data in grouped_data]


      # Implement pagination
    paginator = Paginator(analytics_data, 10) #00items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    # Pass the data to the template
    context = {
        'analytics_data': page_obj,  # Use this for displaying full data
        'data': grouped_data,
        'total_visits': total_visits,
        'filter_type': filter_type,
        'labels': labels,
        'clicks': clicks,
         'page_obj': page_obj,
    }
    return render(request, 'admin_kt/user_dashboard.html', context)
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
# @user_passes_test(admin_required, login_url='/login/')
#  def analytics_dashboard(request):
#     data = WebsiteAnalytics.objects.filter(page_url='https://www.kataktravel.com').order_by('-timestamp')
#     total_visits = data.count()
#     return render(request, 'analytics/analytics_dashboard.html', {'data': data, 'total_visits': total_visits})
# 