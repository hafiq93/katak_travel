from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, PackageItem, PackageType, Location
from admin_kt.models import MerchantType
from user_kt.models import User
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect


def admin_required(user):
    return user.is_staff


@user_passes_test(admin_required, login_url='/login/')
def pack_list_add(request, id=None):
    if request.method == "POST":
        name = request.POST.get('hotel_name')  # Package name
        min_pax = int(request.POST.get('min_pax'))
        max_pax = int(request.POST.get('max_pax'))
        description = request.POST.get('description', '')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        user_pic = request.user  # Set the user who created the package

        location_country = request.POST.get('location')  # Get country (location)
        city_name = request.POST.get('city')  # City

        try:
            location = Location.objects.get(country=location_country)
        except Location.DoesNotExist:
            location = None

        if not location:
            messages.error(request, 'Please provide a valid location.')
        elif min_pax > max_pax:
            messages.error(request, 'Minimum Pax cannot be greater than Maximum Pax.')
        else:
            if id:  # Update an existing package
                package = Package.objects.get(id=id)
                package.name = name
                package.location = location
                package.city = city_name
                package.min_pax = min_pax
                package.max_pax = max_pax
                package.description = description
                package.start_date = start_date
                package.end_date = end_date
                package.user_pic = user_pic  # Ensure this is set during update
                package.save()
                messages.success(request, 'Package updated successfully!')
            else:  # Create a new package
                package = Package.objects.create(
                    name=name,
                    location=location,
                    city=city_name,
                    min_pax=min_pax,
                    max_pax=max_pax,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    user_pic=user_pic,  # Set the user who created the package
                )
                messages.success(request, 'Package added successfully!')
            
            # Redirect back to the same page with the newly created or updated package
            return redirect('pack_list_add', id=package.id)

    # Fetch package for pre-population of the form if ID exists
    package = None
    if id:
        try:
            package = Package.objects.get(id=id)
        except Package.DoesNotExist:
            package = None

    package_types = PackageType.objects.all()
    locations = Location.objects.all()

    return render(request, 'pack_list_kt/package_add.html', {
        'package_types': package_types,
        'locations': locations,
        'package': package,  # Pass the current package to the template
    })


def active_packages(request):
    packages = Package.objects.filter(status='active', end_date__gte=timezone.now().date())
    return render(request, 'package_list.html', {'packages': packages})


def expire_packages():
    Package.objects.filter(end_date__lt=timezone.now().date()).update(status='expired')

@user_passes_test(admin_required, login_url='/login/')
def pack_list_add_items(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == "POST":
        name = request.POST.get('item_name')
        merchant_price = request.POST.get('merchant_price')
        selling_price = request.POST.get('selling_price')
        commission_percent = request.POST.get('commission_percent')

        # Save package item
        PackageItem.objects.create(
            package=package,
            name=name,
            merchant_price=merchant_price,
            selling_price=selling_price,
            commission_percent=commission_percent,
        )
        return redirect('pack_list_add_items', package_id=package.id)

    items = package.items.all()
    total_merchant_price = sum(item.merchant_price for item in items)
    total_selling_price = sum(item.selling_price for item in items)
    total_commission = sum(item.commission_amount() for item in items)

    context = {
        'package': package,
        'items': items,
        'total_merchant_price': total_merchant_price,
        'total_selling_price': total_selling_price,
        'total_commission': total_commission,
    }
    return render(request, 'pack_list_kt/package_add_items.html', context)


@user_passes_test(admin_required, login_url='/login/')
def pack_merchant(request, id):
    package = get_object_or_404(Package, id=id)  # Fetch the package using the id
    merchant_types = MerchantType.objects.all()  # Get all merchant types
    user_pic = request.user  # If you want the logged-in user
    return render(request, 'pack_list_kt/package_merchant.html', {
        'package': package, 'merchant_types': merchant_types,'user_pic': user_pic,})