from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, PackageItem, PackageType, Location,MerchantPackage,PackageMerchant
from admin_kt.models import  MainMerchant, MerchantType
from user_kt.models import User
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
# from django_countries.fields import CountryField  # Optional for country selection


def admin_required(user):
    return user.is_staff


@user_passes_test(admin_required, login_url='/login/')
def pack_list_add(request, id=None):
    if request.method == "POST":
        name = request.POST.get('hotel_name')  # Package name
        min_pax = int(request.POST.get('min_pax'))
        max_pax = int(request.POST.get('max_pax'))
        description = request.POST.get('description', '')
        info = request.POST.get('info', '')  # New field for info
        date_of_travel = request.POST.get('date_of_travel', '')  # New field for date_of_travel
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        code = request.POST.get('code')

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
                package.info = info  # Update info
                package.date_of_travel = date_of_travel  # Update date_of_travel
                package.start_date = start_date
                package.end_date = end_date
                package.code = code
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
                    code=code,
                    description=description,
                    info=info,  # Save info
                    date_of_travel=date_of_travel,  # Save date_of_travel
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



def pack_merchant(request, id):
    # Retrieve the package based on the ID
    package = get_object_or_404(Package, id=id)

    # Get all countries from the Location model
    countries = Location.objects.all()

    if request.method == 'POST':
        # Extract user input from the POST request
        merchant_name = request.POST.get('merchant_name')  # Merchant name
        merchant_code = request.POST.get('merchant_code')  # Merchant code
        merchant_type_id = request.POST.get('merchant_type')  # Merchant type ID
        
        # Address and contact fields
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country_name = request.POST.get('country')  # Get the country name from the form
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Product details fields
        product_name = request.POST.get('product_name')  # Product name
        product_description = request.POST.get('product_description')  # Product description
        product_image = request.FILES.get('product_image')  # Image upload field for product image

        # Retrieve or create the Location instance for the country
        country_instance, _ = Location.objects.get_or_create(country=country_name)

        # Create or retrieve a MerchantPackage
        merchant_package, created = MerchantPackage.objects.get_or_create(
            merchant=merchant_name,
            defaults={
                'street_address': street_address,
                'city': city,
                'state': state,
                'postal_code': postal_code,
                'country': country_instance,  # Assign the Location instance
                'contact_person': contact_person,
                'contact_number': contact_number,
                'email': email,
            }
        )

        # If the MerchantPackage already exists but we need to update optional fields:
        if not created:
            MerchantPackage.objects.filter(id=merchant_package.id).update(
                street_address=street_address or merchant_package.street_address,
                city=city or merchant_package.city,
                state=state or merchant_package.state,
                postal_code=postal_code or merchant_package.postal_code,
                country=country_instance or merchant_package.country,  # Update the Location instance
                contact_person=contact_person or merchant_package.contact_person,
                contact_number=contact_number or merchant_package.contact_number,
                email=email or merchant_package.email,
            )

        # Create a new PackageMerchant record
        merchant = PackageMerchant.objects.create(
            package=package,
            name=merchant_name,
            merchant_code=merchant_code,
            merchant_type_id=merchant_type_id,
            merchant_list=merchant_package  # Assign the MerchantPackage instance
        )

        # Create ProductDetails for the new merchant (if product details were provided)
        if product_name and product_description:
            product_details = ProductDetails.objects.create(
                product_name=product_name,
                product_description=product_description,
                product_image=product_image,  # This will save the uploaded image
                package_merchant=merchant  # Associate it with the newly created PackageMerchant
            )

        # Redirect to the next page after saving
        return redirect('pack_price', package_id=package.id)

    # If the request is not POST, render the merchant form template
    return render(request, 'pack_list_kt/package_merchant.html', {
        'package': package,
        'merchant_types': MerchantType.objects.all(),  # Pass merchant types for the dropdown
        'countries': countries,  # Pass countries for the dropdown
    })
    

def pack_mer_edit(request, merchant_id):
    merchant = get_object_or_404(PackageMerchant, id=merchant_id)
    package = merchant.package  # Assuming the relationship exists

    if request.method == 'POST':
        merchant.selling_price = request.POST.get('selling_price')
        merchant.agent_price = request.POST.get('agent_price')
        merchant.save()
        return redirect('package_merc_edit', package_id=package.id)

    return render(request, 'pack_list_kt/package_merc_edit.html', {
        'merchant': merchant,
        'package': package,
    })



def delete_merchant(request, id):
    merchant = get_object_or_404(PackageMerchant, id=id)
    merchant.delete()
    return JsonResponse({'success': True})

def get_merchant(request, id):
    merchant = get_object_or_404(PackageMerchant, id=id)
    return JsonResponse({
        'name': merchant.name,
        'type_id': merchant.merchant_type.id if merchant.merchant_type else ''
    })

def pack_price(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    

    if request.method == 'POST':
        merchant_name = request.POST.get('merchant_name')
        merchant_code = request.POST.get('merchant_code')
        merchant_type_id = request.POST.get('merchant_type')
        selling_price = request.POST.get('selling_price')
        agent_price = request.POST.get('agent_price')
        commission = request.POST.get('commission')

        if not merchant_name:
            return JsonResponse({'success': False, 'error': 'Merchant name is required.'}, status=400)

        merchant_package, created = MerchantPackage.objects.get_or_create(
            merchant_name=merchant_name
        )

        merchant = PackageMerchant.objects.create(
            package=package,
            merchant_list=merchant_package,
            merchant_code=merchant_code,
            merchant_type_id=merchant_type_id,
        )

        PackageItem.objects.create(
            merchant_list=merchant,
            name=f'{merchant_name} Item',
            merchant_price=agent_price,
            selling_price=selling_price,
            commission_percent=commission,
        )

        return JsonResponse({
            'success': True,
            'merchant': {
                'id': merchant.id,
                'name': merchant.merchant_list.merchant,
                'type': merchant.merchant_type.name if merchant.merchant_type else "N/A",
                'code': merchant.merchant_code,
                'selling_price': merchant.selling_price,
                'agent_price': merchant.agent_price,
                'commission': merchant.commission,
            }
        })

    return render(request, 'pack_list_kt/package_price.html', {
        'package': package,
        'merchant_types': MerchantType.objects.all(),
    })


def get_merchant_details(request, id):
    try:
        merchant = PackageMerchant.objects.get(id=id)
        return JsonResponse({
            'success': True,
            'merchant': {
                'name': merchant.merchant_list.merchant,
                'code': merchant.merchant_code,
                'type': merchant.merchant_type.name if merchant.merchant_type else "N/A",
            }
        })
    except PackageMerchant.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Merchant not found'}, status=404)



def pack_form(request, merchant_id):  # Change `package_id` to `merchant_id`
    # Retrieve the PackageMerchant by ID
    package_merchant = get_object_or_404(PackageMerchant, id=merchant_id)
    merchant = package_merchant.merchant_list  # Get the related MerchantPackage

    # Get all countries from the Location model
    countries = Location.objects.all()
    merchant_types = MerchantType.objects.all()  # Get all merchant types

    if request.method == 'POST':
        # Extract user input from the POST request
        merchant_name = request.POST.get('merchant_name')
        merchant_code = request.POST.get('merchant_code')
        merchant_type_id = request.POST.get('merchant_type')

        # Address and contact fields
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country_name = request.POST.get('country')
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Product details fields
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_image = request.FILES.get('product_image')

        # Retrieve or create the Location instance for the country
        country_instance, _ = Location.objects.get_or_create(country=country_name)

        # Update the MerchantPackage
        merchant.street_address = street_address
        merchant.city = city
        merchant.state = state
        merchant.postal_code = postal_code
        merchant.country = country_instance
        merchant.contact_person = contact_person
        merchant.contact_number = contact_number
        merchant.email = email
        merchant.save()

        # Update ProductDetails if product data is provided
        if product_name and product_description:
            ProductDetails.objects.update_or_create(
                package_merchant=package_merchant,
                defaults={'product_name': product_name, 'product_description': product_description, 'product_image': product_image},
            )

        # Redirect to the next page after saving
        return redirect('pack_price', package_id=package_merchant.package.id)

    return render(request, 'pack_list_kt/package_form.html', {
        'package': package_merchant.package,
        'merchant': merchant,
        'merchant_types': merchant_types,
        'countries': countries,
    })