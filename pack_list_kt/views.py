from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, PackageItem, PackageType, Location,MerchantPackage,PackageMerchant,ProductDetails,ProductItemTotal,PackageItemTotalLink,PackageLog,PackCategory  
from admin_kt.models import  MainMerchant, MerchantType, Status,Roles,UserRole
from user_kt.models import User
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest
from decimal import Decimal, InvalidOperation

# import logging
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Sum
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# from django_countries.fields import CountryField  # Optional for country selection

# Set up logging
# logger = logging.getLogger(__name__)


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

        merchant_type_id = request.POST.get('merchant_type')
        merchant_type = None
        if merchant_type_id:
            try:
                merchant_type = MerchantType.objects.get(id=merchant_type_id)
            except MerchantType.DoesNotExist:
                merchant_type = None

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

                # Delete and recreate PackCategory
                PackCategory.objects.filter(package=package).delete()
                if merchant_type:
                    PackCategory.objects.create(package=package, merchant_type=merchant_type)

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
                if merchant_type:
                    PackCategory.objects.create(package=package, merchant_type=merchant_type)

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
    merchant_types = MerchantType.objects.all()

    return render(request, 'pack_list_kt/package_add.html', {
        'package_types': package_types,
        'locations': locations,
        'package': package,  # Pass the current package to the template
        'merchant_types': merchant_types,
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


# form merchant in update
def pack_merchant(request, id):
    package = get_object_or_404(Package, id=id)
    countries = Location.objects.all()

    if request.method == 'POST':
        # Retrieve merchant details from the form
        merchant_name = request.POST.get('merchant_name')
        merchant_code = request.POST.get('merchant_code')
        merchant_type_id = request.POST.get('merchant_type')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country_name = request.POST.get('country')
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Retrieve or create the Location instance for the country
        country_instance, _ = Location.objects.get_or_create(country=country_name)

        # Create or retrieve the MerchantPackage
        merchant_package, created = MerchantPackage.objects.get_or_create(
            merchant=merchant_name,
            defaults={
                'street_address': street_address,
                'city': city,
                'state': state,
                'postal_code': postal_code,
                'country': country_instance,
                'contact_person': contact_person,
                'contact_number': contact_number,
                'email': email,
            }
        )

        if not created:
            # Update existing MerchantPackage with new information
            MerchantPackage.objects.filter(id=merchant_package.id).update(
                street_address=street_address,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country_instance,
                contact_person=contact_person,
                contact_number=contact_number,
                email=email
            )

        # Create PackageMerchant connection between the package and the merchant
        merchant = PackageMerchant.objects.create(
            package=package,
            merchant_code=merchant_code,
            merchant_type_id=merchant_type_id,
            merchant_list=merchant_package
        )

        # Handle the products added to the merchant package
        product_names = request.POST.getlist('product_name[]')
        product_descriptions = request.POST.getlist('product_description[]')
        product_images = request.FILES.getlist('product_image[]')

        for i in range(len(product_names)):
            # Ensure that the image exists and is within the size limit
            if product_images and product_images[i].size > 400 * 1024:  # 400KB limit
                messages.error(request, f"Image file size exceeds 400KB for product: {product_names[i]}.")
                continue

            if product_images and not product_images[i].name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                messages.error(request, f"Invalid file type for product: {product_names[i]}. Only JPG, JPEG, PNG, GIF, and WEBP are allowed.")
                continue

            # Save product details with conditional fields
            ProductDetails.objects.create(
                product_name=product_names[i] if i < len(product_names) else None,
                product_description=product_descriptions[i] if i < len(product_descriptions) else None,
                product_image=product_images[i] if i < len(product_images) else None,
                package_merchant=merchant
            )

        messages.success(request, 'Package and products have been saved successfully.')
         # Get the first product linked to the merchant, or create a new one
        first_product = ProductDetails.objects.filter(package_merchant=merchant).first()
        
        if first_product:
            return redirect('add_price', product_id=first_product.id)
        else:
            return redirect('pack_price', package_id=package.id)  # Fallback if no product exists

    # Render the form for creating/editing a merchant package
    context = {
        'package': package,
        'merchant_types': MerchantType.objects.all(),
        'countries': countries,
    }
    return render(request, 'pack_list_kt/package_merchant.html', context)
    

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


@user_passes_test(admin_required, login_url='/login/')
def update_package_status(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        status_id = request.POST.get('status')
        remarks = request.POST.get('remarks')
        send_to_id = request.POST.get('send_to')  # 👈 NEW LINE

        status = get_object_or_404(Status, id=status_id)
        from_user_role = UserRole.objects.filter(user=request.user).first()
        to_user_role = UserRole.objects.filter(id=send_to_id).first()  # 👈 NEW LINE

        PackageLog.objects.create(
            package=package,
            status=status,
            remarks=remarks,
            updated_at=timezone.now(),
            from_user_role=from_user_role,  # 👈 NEW LINE
            to_user_role=to_user_role      # 👈 NEW LINE
        )

        package.pack_status = status
        package.save()

        return redirect('package_all_details', package_id=package_id)

    return redirect('pack_price', package_id=package_id)

@user_passes_test(admin_required, login_url='/login/')
def pack_price(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    # Get total price
    price_subquery = ProductItemTotal.objects.filter(
        merchant=OuterRef('pk')
    ).values('total_selling_price')[:1]

    package_merchants = package.package_merchants.annotate(
        total_selling_price=Subquery(price_subquery)
    )

    package_total_price = package_merchants.aggregate(
        total_price=Sum('total_selling_price')
    )['total_price'] or 0.00

    merchant_types = MerchantType.objects.all()
    countries = Location.objects.all()
    package_merchant = package.package_merchants.first()
    if not package_merchant:
        return redirect('error_page')

    merchant = package_merchant.merchant_list
    statuses = Status.objects.all()

    product_details = ProductDetails.objects.filter(package_merchant=package_merchant)
    package_items = PackageItem.objects.filter(merchant_list=package_merchant)
    product = product_details.first() if product_details.exists() else None
    product_total = ProductItemTotal.objects.filter(merchant=package_merchant).last()

    allowed_roles = Roles.objects.filter(can_receive_status_update=True)
    send_to_userroles = UserRole.objects.filter(role__in=allowed_roles).select_related('user', 'role')

    context = {
        'package': package,
        'merchant_types': merchant_types,
        'package_merchants': package_merchants,
        'package_total_price': package_total_price,
        'package_merchant': package_merchant,
        'merchant': merchant,
        'product_details': product_details,
        'package_items': package_items,
        'product': product,
        'product_total': product_total,
        'countries': countries,
        'statuses': statuses,
        'current_status': package.pack_status,
        'send_to_userroles': send_to_userroles,
    }

    return render(request, 'pack_list_kt/package_price.html', context)

def duplicate_merchant(request, id):
    merchant = get_object_or_404(PackageMerchant, id=id)

    if request.method == "POST":
        # Create a duplicate
        new_merchant = PackageMerchant.objects.create(
            package=merchant.package,
            merchant_list=merchant.merchant_list,
            merchant_code=merchant.merchant_code + "_copy",
            merchant_type=merchant.merchant_type,
        )
        messages.success(request, "Merchant duplicated successfully!")
        return redirect('pack_price', package_id=merchant.package.id)

    return HttpResponse("Invalid request", status=400)

def delete_merchant_new(request, id):
    merchant = get_object_or_404(PackageMerchant, id=id)

    if request.method == "POST":
        package_id = merchant.package.id  # Get package_id before deleting
        merchant.delete()
        messages.success(request, "Merchant deleted successfully!")
        return redirect('pack_price', package_id=package_id)

    return HttpResponse("Invalid request", status=400)

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


def pack_form(request, merchant_id):
    # Retrieve the PackageMerchant by ID
    package_merchant = get_object_or_404(PackageMerchant, id=merchant_id)
    merchant = package_merchant.merchant_list  # Get the related MerchantPackage

    # Get all countries and merchant types
    countries = Location.objects.all()
    merchant_types = MerchantType.objects.all()

    # Retrieve associated ProductDetails and PackageItems
    product_details = ProductDetails.objects.filter(package_merchant=package_merchant)
    package_items = PackageItem.objects.filter(merchant_list=package_merchant)

    # Fetch the first product if available
    product = product_details.first() if product_details.exists() else None

    # Fetch the latest ProductItemTotal for this merchant
    product_total = ProductItemTotal.objects.filter(merchant=package_merchant).last()

    if request.method == "POST":
        # Calculate total selling price from PackageItem
        total_selling_price = package_items.aggregate(
            total=Sum('grand_total_price')
        )['total'] or Decimal('0.00')

        if product_total:
            # Update existing ProductItemTotal
            product_total.total_selling_price = total_selling_price
            product_total.save()
        else:
            # Create a new ProductItemTotal record linked to the merchant
            try:
                product_total = ProductItemTotal.objects.create(
                    merchant=package_merchant,
                    total_selling_price=total_selling_price
                )
            except IntegrityError as e:
                if '1062' in str(e):
                    print("Duplicate entry error: ", e)
                    return redirect('error_page')

        # Link PackageItem to ProductItemTotal through PackageItemTotalLink
        for package_item in package_items:
            PackageItemTotalLink.objects.get_or_create(
                package_item=package_item,
                product_item_total=product_total
            )

        return redirect('pack_form', merchant_id=merchant_id)  # Redirect back to the same page

    return render(request, 'pack_list_kt/package_form.html', {
        'package': package_merchant.package,
        'merchant': merchant,
        'merchant_types': merchant_types,
        'countries': countries,
        'package_merchant': package_merchant,
        'product_details': product_details,
        'package_items': package_items,
        'product': product,
        'product_total': product_total,  # Pass the total to the template
    })

def delete_product(request, product_id):
    if request.method == 'DELETE':
        product_item = get_object_or_404(PackageItem, id=product_id)
        product_item.delete()  # Delete the product
        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'status': 'error'}, status=400)

def product_pricing_view(request):
    # Get the product and package details
    product_details = Product.objects.all()  # Adjust your query
    package_items = PackageItem.objects.all()  # Adjust your query
    
    # Set up pagination
    paginator = Paginator(product_details, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass data to the template
    return render(request, 'package_form.html', {'page_obj': page_obj, 'package_items': package_items})

def sanitize_price(value):
    """
    This function removes commas from price values (e.g., "1,000.00" becomes "1000.00")
    before attempting to convert them to Decimal. Returns Decimal('0.00') if input is invalid.
    """
    if value:
        try:
            value = value.replace(",", "")  # Remove commas
            return Decimal(value)  # Attempt to convert to Decimal
        except (ValueError, InvalidOperation):
            return Decimal('0.00')  # Return a default value in case    of conversion failure
    return Decimal('0.00')  # Default value for None or empty input


def add_price(request, product_id):
    """
    This view handles the addition or update of pricing details for a product.
    It also fetches related PackageItem data for GET requests.
    """
    product = get_object_or_404(ProductDetails, id=product_id)

    if request.method == 'POST':
        try:
            # Update basic product details
            product.product_name = request.POST.get('product_name')
            product.product_description = request.POST.get('product_description')

            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']

            # Fetch and sanitize pricing details
            adult_selling_price = Decimal(sanitize_price(request.POST.get('adult_selling_price', '0.00')))
            adult_agent_price = Decimal(sanitize_price(request.POST.get('adult_agent_price', '0.00')))
            children_selling_price = Decimal(sanitize_price(request.POST.get('children_selling_price', '0.00')))
            children_agent_price = Decimal(sanitize_price(request.POST.get('children_agent_price', '0.00')))

            # Fetch number of adults and children safely
            adult_number = int(request.POST.get('adult_number', '0') or '0')
            children_number = int(request.POST.get('children_number', '0') or '0')

            # Validate pricing values (Ensure non-negative values)
            if any(v < 0 for v in [adult_selling_price, adult_agent_price, children_selling_price, children_agent_price]):
                raise ValueError("Pricing values must be non-negative.")

            # Calculate commission details for adults and children
            adult_commission_price = adult_selling_price - adult_agent_price
            adult_commission_percent = (adult_commission_price / adult_selling_price) * 100 if adult_selling_price else 0

            children_commission_price = children_selling_price - children_agent_price
            children_commission_percent = (children_commission_price / children_selling_price) * 100 if children_selling_price else 0

            # Save updated product details
            product.save()

            # Get or create the PackageItem instance
            package_item, created = PackageItem.objects.get_or_create(product_details=product)

            # Assign values to PackageItem
            package_item.adult_number = adult_number
            package_item.adult_selling_price = adult_selling_price
            package_item.adult_agent_price = adult_agent_price
            package_item.adult_commission_price = adult_commission_price
            package_item.adult_commission_percent = adult_commission_percent

            package_item.children_number = children_number
            package_item.children_selling_price = children_selling_price
            package_item.children_agent_price = children_agent_price
            package_item.children_commission_price = children_commission_price
            package_item.children_commission_percent = children_commission_percent

            # Assign merchant list from ProductDetails
            package_item.merchant_list = product.package_merchant

            # Save the PackageItem (Wrap in try-except to catch errors)
            try:
                package_item.save()
            except Exception as e:
                logger.error(f"Error saving PackageItem: {e}")
                return HttpResponseBadRequest(f"Failed to save package item. Error: {e}")

            # Redirect after success
            return redirect('pack_form', merchant_id=product.package_merchant.id)

        except (ValueError, InvalidOperation) as e:
            logger.error(f"Invalid pricing data received: {e}")
            return HttpResponseBadRequest(f"Invalid data received for pricing details. Error: {e}")

    # Handle GET request
    package_items = PackageItem.objects.filter(product_details=product)

    if package_items.exists():
        package_item = package_items.first()  # Get the first object
    else:
        package_item = None

    # Prepare context for rendering
    context = {
        'product': product,
        'package_item': package_item,
        'adult_selling_price': package_item.adult_selling_price if package_item else Decimal('0.00'),
        'adult_agent_price': package_item.adult_agent_price if package_item else Decimal('0.00'),
        'children_selling_price': package_item.children_selling_price if package_item else Decimal('0.00'),
        'children_agent_price': package_item.children_agent_price if package_item else Decimal('0.00'),
        'adult_number': package_item.adult_number if package_item else 0,
        'children_number': package_item.children_number if package_item else 0,
        'adult_commission_price': package_item.adult_commission_price if package_item else Decimal('0.00'),
        'adult_commission_percent': package_item.adult_commission_percent if package_item else Decimal('0.00'),
        'children_commission_price': package_item.children_commission_price if package_item else Decimal('0.00'),
        'children_commission_percent': package_item.children_commission_percent if package_item else Decimal('0.00'),
        'total_adult_price': package_item.total_adult_price if package_item else Decimal('0.00'),
        'total_children_price': package_item.total_children_price if package_item else Decimal('0.00'),
        'grand_total_price': package_item.grand_total_price if package_item else Decimal('0.00'),
    }

    # Render the template
    return render(request, 'pack_list_kt/package_add_price.html', context)



# for add product button
def add_product(request, product_id):
    """
    Handles adding multiple products and updating pricing details.
    """
    print(f"Request method: {request.method}")  # Debugging
    product = get_object_or_404(ProductDetails, id=product_id)

    package_item = None  # Ensure package_item is always defined

    if request.method == 'POST':
        print("Form submitted!")  # Debugging
        print(f"POST data: {request.POST}")  # Debugging
        print(f"FILES data: {request.FILES}")  # Debugging

        # Handle multiple product additions
        product_names = request.POST.getlist('product_name[]')
        product_descriptions = request.POST.getlist('product_description[]')
        product_images = request.FILES.getlist('product_image[]')

        for i in range(len(product_names)):
            product_image = product_images[i] if i < len(product_images) else None

            # Validate image
            if product_image:
                if product_image.size > 400 * 1024:  # 400KB limit
                    print(f"Image size exceeds 400KB for product: {product_names[i]}")  # Debugging
                    messages.error(request, f"Image file size exceeds 400KB for product: {product_names[i]}.")
                    continue
                if not product_image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    print(f"Invalid file type for product: {product_names[i]}")  # Debugging
                    messages.error(request, f"Invalid file type for product: {product_names[i]}.")
                    continue

            try:
                # Save product details
                new_product = ProductDetails.objects.create(
                    product_name=product_names[i] if i < len(product_names) else None,
                    product_description=product_descriptions[i] if i < len(product_descriptions) else None,
                    product_image=product_image,
                    package_merchant=product.package_merchant
                )
                print(f"Product created: {new_product.id}")  # Debugging

                # Handle price addition
                adult_selling_price = Decimal(sanitize_price(request.POST.get('adult_selling_price', '0.00')))
                adult_agent_price = Decimal(sanitize_price(request.POST.get('adult_agent_price', '0.00')))
                children_selling_price = Decimal(sanitize_price(request.POST.get('children_selling_price', '0.00')))
                children_agent_price = Decimal(sanitize_price(request.POST.get('children_agent_price', '0.00')))

                adult_number = int(request.POST.get('adult_number', 0))
                children_number = int(request.POST.get('children_number', 0))

                # Validate pricing data (no negative prices allowed)
                if any(v < 0 for v in [adult_selling_price, adult_agent_price, children_selling_price, children_agent_price]):
                    print("Pricing values must be non-negative.")  # Debugging
                    messages.error(request, "Pricing values must be non-negative.")
                    continue

                # Calculate commission prices and percentages
                adult_commission_price = adult_selling_price - adult_agent_price
                adult_commission_percent = (adult_commission_price / adult_selling_price) * 100 if adult_selling_price else 0

                children_commission_price = children_selling_price - children_agent_price
                children_commission_percent = (children_commission_price / children_selling_price) * 100 if children_selling_price else 0

                # Create or update PackageItem instance
                package_item, created = PackageItem.objects.get_or_create(product_details=new_product)
                package_item.adult_number = adult_number
                package_item.adult_selling_price = adult_selling_price
                package_item.adult_agent_price = adult_agent_price
                package_item.adult_commission_price = adult_commission_price
                package_item.adult_commission_percent = adult_commission_percent
                package_item.children_number = children_number
                package_item.children_selling_price = children_selling_price
                package_item.children_agent_price = children_agent_price
                package_item.children_commission_price = children_commission_price
                package_item.children_commission_percent = children_commission_percent
                package_item.merchant_list = new_product.package_merchant
                package_item.save()

                # **Create ProductItemTotal and link it to PackageItemTotalLink**
                product_item_total, _ = ProductItemTotal.objects.get_or_create(
                    product_details=new_product
                )

                # **Create PackageItemTotalLink**
                package_item_total_link = PackageItemTotalLink.objects.create(
                    package_item=package_item,
                    product_item_total=product_item_total,
                    quantity=1
                )

                print(f"PackageItem saved for product: {new_product.id}")  # Debugging
                messages.success(request, f"Product '{new_product.product_name}' added successfully!")

            except Exception as e:
                print(f"Error saving product or package item: {e}")  # Debugging
                messages.error(request, f"Invalid pricing data for product: {product_names[i]}. Error: {e}")
                continue

        print(f"Redirecting to pack_form with merchant_id: {product.package_merchant.id}")  # Debugging
        return redirect('pack_form', merchant_id=product.package_merchant.id)

    context = {
        'product': product,
        'package_item': package_item,
        'adult_selling_price': package_item.adult_selling_price if package_item else 0.00,
        'adult_agent_price': package_item.adult_agent_price if package_item else 0.00,
        'children_selling_price': package_item.children_selling_price if package_item else 0.00,
        'children_agent_price': package_item.children_agent_price if package_item else 0.00,
        'adult_number': package_item.adult_number if package_item else 0,
        'children_number': package_item.children_number if package_item else 0,
        'adult_commission_price': package_item.adult_commission_price if package_item else 0.00,
        'adult_commission_percent': package_item.adult_commission_percent if package_item else 0.00,
        'children_commission_price': package_item.children_commission_price if package_item else 0.00,
        'children_commission_percent': package_item.children_commission_percent if package_item else 0.00,
        'total_adult_price': package_item.total_adult_price if package_item else 0.00,
        'total_children_price': package_item.total_children_price if package_item else 0.00,
        'grand_total_price': package_item.grand_total_price if package_item else 0.00,
    }
    return render(request, 'pack_list_kt/package_add_product.html', context)


    


def products_details(request, product_id):
    product = get_object_or_404(ProductDetails, id=product_id)

    # Fetch related PackageItem data
    try:
        package_item = PackageItem.objects.get(product_details=product)
    except PackageItem.DoesNotExist:
        package_item = None

    # Prepare context for rendering
    context = {
        'product': product,
        'package_item': package_item,
        'adult_selling_price': package_item.adult_selling_price if package_item else 0.00,
        'adult_agent_price': package_item.adult_agent_price if package_item else 0.00,
        'children_selling_price': package_item.children_selling_price if package_item else 0.00,
        'children_agent_price': package_item.children_agent_price if package_item else 0.00,
        'adult_number': package_item.adult_number if package_item else 0,
        'children_number': package_item.children_number if package_item else 0,
        'adult_commission_price': package_item.adult_commission_price if package_item else 0.00,
        'adult_commission_percent': package_item.adult_commission_percent if package_item else 0.00,
        'children_commission_price': package_item.children_commission_price if package_item else 0.00,
        'children_commission_percent': package_item.children_commission_percent if package_item else 0.00,
        'total_adult_price': package_item.total_adult_price if package_item else 0.00,
        'total_children_price': package_item.total_children_price if package_item else 0.00,
        'grand_total_price': package_item.grand_total_price if package_item else 0.00,
    }

    # Render the template with the context
    return render(request, 'pack_list_kt/package_details.html', context)

def package_all_details(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    # Get the subquery for price
    price_subquery = ProductItemTotal.objects.filter(
        merchant=OuterRef('pk')
    ).values('total_selling_price')[:1]

    # Annotate the package_merchants queryset with total_selling_price
    package_merchants = package.package_merchants.annotate(
        total_selling_price=Subquery(price_subquery)
    )

    # Calculate total package price
    package_total_price = package_merchants.aggregate(
        total_price=Sum('total_selling_price')
    )['total_price'] or Decimal('0.00')

    merchant_types = MerchantType.objects.all()
    countries = Location.objects.all()

    # Retrieve the first PackageMerchant if it exists
    package_merchant = package.package_merchants.first()
    if not package_merchant:
        return redirect('error_page')  # Redirect if no PackageMerchant found

    merchant = package_merchant.merchant_list
    statuses = Status.objects.all()

    # Retrieve associated ProductDetails and PackageItems
    product_details = ProductDetails.objects.filter(package_merchant=package_merchant)
    package_items = PackageItem.objects.filter(merchant_list=package_merchant)

    # Fetch the first product if available
    product = product_details.first() if product_details.exists() else None

    # Fetch the latest ProductItemTotal for this merchant
    product_total = ProductItemTotal.objects.filter(merchant=package_merchant).last()

    # Retrieve all PackageLogs related to this package
    package_logs = PackageLog.objects.filter(package=package).order_by('updated_at')

    # Ensure to check if package_logs.exists() before accessing the first element
    if package_logs.exists():
        to_user_role = package_logs.first().to_user_role
        if to_user_role:
            to_user_username = to_user_role.user.username  # Access the username of the related user
            print(f"To User Role Username: {to_user_username}")
        else:
            print("To User Role is None.")
    else:
        print("No package logs found.")

    # Check if the user is authenticated before accessing user-specific data
    if not request.user.is_authenticated:
        # Handle the case for unauthenticated users (e.g., redirect to login page)
        return redirect('login')  # Redirect to login page if user is not authenticated

    # Retrieve the current user's role in the package (only if the user is authenticated)
    current_user_role = UserRole.objects.filter(user=request.user).first()  # Get the role for the current logged-in user
    
    # Get the to_user_role and from_user_role from the first package log
    to_user_role = package_logs.first().to_user_role if package_logs.exists() else None
    from_user_role = package_logs.first().from_user_role if package_logs.exists() else None

    # Safely access to_user_username only if to_user_role exists
    to_user_username = to_user_role.user.username if to_user_role else None

    package_log = package_logs.first() if package_logs.exists() else None

    # Get the user role of the sender (the one who sent it to me)
    send_back_userroles = []
    if package_log and package_log.from_user_role:
        send_back_userroles = [package_log.from_user_role]  # Make it a list for consistency


    context = {
        'package': package,
        'merchant_types': merchant_types,
        'package_merchants': package_merchants,
        'package_total_price': package_total_price,
        'package_merchant': package_merchant,
        'merchant': merchant,
        'product_details': product_details,
        'package_items': package_items,
        'product': product,
        'product_total': product_total,
        'countries': countries,
        'statuses': statuses,  # 👈 all available status options
        'current_status': package.pack_status,  # 👈 current status for the package
        'package_logs': package_logs,  # 👈 add package logs here
        'current_user_role': current_user_role,
        'to_user_role': to_user_role,
        'from_user_role': from_user_role,
        'to_user_username': to_user_username,  # Add the username to context
        'package_log':package_log,
        'send_back_userroles': send_back_userroles,
    }

    return render(request, 'pack_list_kt/package_all_details.html', context)

@user_passes_test(admin_required, login_url='/login/')
def send_back(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        send_to_user_id = request.POST.get('send_to')
        remarks = request.POST.get('remarks')
        new_status_id = request.POST.get('status')  # Get new status if needed

        if send_to_user_id:
            # Get the 'send_to' user role object
            send_to_user_role = UserRole.objects.get(id=send_to_user_id)

            # Fetch the latest PackageLog entry to get the from_user_role
            last_package_log = PackageLog.objects.filter(package=package).order_by('-updated_at').first()

            if last_package_log:
                from_user_role = last_package_log.to_user_role  # Use the last 'to_user_role' as the 'from_user_role'
                to_user_role = send_to_user_role  # Set the new recipient user role

                # Update the package's user role (sending it back to the previous user)
                package.to_user_role = send_to_user_role

                # If a new status is selected (i.e., a "send-back" status), change it
                if new_status_id:
                    new_status = get_object_or_404(Status, id=new_status_id)
                    package.pack_status = new_status  # Set the new status for the package
                else:
                    # Optionally, use the last package status if no new status is provided
                    package.pack_status = last_package_log.status

                # Save the updated package
                package.save()

                # Log the action in PackageLog
                PackageLog.objects.create(
                    package=package,
                    from_user_role=from_user_role,
                    to_user_role=send_to_user_role,
                    status=package.pack_status,  # Set the current status for the log
                    remarks=remarks,
                    updated_at=timezone.now(),  # Log the time
                )

                # Optionally, notify the user
                messages.success(request, f"Package sent back to {send_to_user_role.user.username}.")
                return redirect('package_all_details', package_id=package.id)
            else:
                messages.error(request, "No previous logs found for this package.")
                return redirect('package_all_details', package_id=package.id)
        else:
            messages.error(request, "Please select a user to send the package back to.")
            return redirect('package_all_details', package_id=package.id)

    # If the method is not POST, redirect back to package details page
    return redirect('package_all_details', package_id=package.id)

@user_passes_test(admin_required, login_url='/login/')
def publish_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    # Check if the package status is "Approved"
    if package.pack_status.name == 'Approved':
        # Change status to "Published"
        published_status = get_object_or_404(Status, name='Published')
        package.pack_status = published_status
        package.save()

        # Log the publish action
        from_user_role = UserRole.objects.filter(user=request.user).first()
        PackageLog.objects.create(
            package=package,
            status=published_status,
            remarks="Package published",
            updated_at=timezone.now(),
            from_user_role=from_user_role,
            to_user_role=from_user_role
        )

        messages.success(request, "Package has been published.")
    else:
        messages.error(request, "Package must be approved first to publish.")

    return redirect('package_all_details', package_id=package.id)


# code use to display in modal
def get_product_details(request, product_id):
    try:
        print(f"🔍 Fetching product details for ID: {product_id}")  # Debugging

        # Fetch product details
        product = get_object_or_404(ProductDetails, id=product_id)

        # Fetch the PackageItem related to the product
        package_item = PackageItem.objects.select_related('merchant_list').filter(product_details=product).first()
        
        if not package_item:
            print("⚠️ No PackageItem found for this product.")
        
        # Fetch the PackageMerchant related to the package item
        package_merchant = package_item.merchant_list if package_item else None
        
        # Check if package_merchant exists before accessing attributes
        package_merchant_data = {}
        if package_merchant:
            package_merchant_data = {
                "merchant_code": getattr(package_merchant, "merchant_code", "N/A"),
                "merchant_type": getattr(package_merchant.merchant_type, "id", "N/A") if package_merchant.merchant_type else "N/A",
            }

        print(f"📦 Package Merchant Data: {package_merchant_data}")  # Debugging

        # Prepare response data
        data = {
            "product_id": product.id,
            "product_name": product.product_name,
            "product_description": product.product_description,
            "image_url": product.product_image.url if product.product_image else "",
            "image_name": product.product_image.name if product.product_image else "",
            "package_merchant": package_merchant_data,
            "adult_selling_price": package_item.adult_selling_price if package_item else 0.00,
            "adult_agent_price": package_item.adult_agent_price if package_item else 0.00,
            "children_selling_price": package_item.children_selling_price if package_item else 0.00,
            "children_agent_price": package_item.children_agent_price if package_item else 0.00,
            "adult_number": package_item.adult_number if package_item else 0,
            "children_number": package_item.children_number if package_item else 0,
            "adult_commission_price": package_item.adult_commission_price if package_item else 0.00,
            "adult_commission_percent": package_item.adult_commission_percent if package_item else 0.00,
            "children_commission_price": package_item.children_commission_price if package_item else 0.00,
            "children_commission_percent": package_item.children_commission_percent if package_item else 0.00,
            "total_adult_price": package_item.total_adult_price if package_item else 0.00,
            "total_children_price": package_item.total_children_price if package_item else 0.00,
            "grand_total_price": package_item.grand_total_price if package_item else 0.00,
        }

        print(f"📤 Returning product details: {data}")  # Debugging
        return JsonResponse(data, safe=False)

    except Exception as e:
        print(f"⚠️ Error fetching product details: {str(e)}")
        return JsonResponse({"error": "Product not found or invalid request"}, status=400)




def get_merchant_product_details(request, merchant_id):
    try:
        # Fetch the PackageMerchant object instead of MerchantPackage
        package_merchant = PackageMerchant.objects.get(id=merchant_id)
        
        # Get the associated MerchantPackage
        merchant = package_merchant.merchant_list
        if not merchant:
            return JsonResponse({"error": f"MerchantPackage for PackageMerchant ID {merchant_id} does not exist."}, status=404)
    
    except PackageMerchant.DoesNotExist:
        return JsonResponse({"error": f"PackageMerchant with id {merchant_id} does not exist."}, status=404)

    # Fetch all PackageMerchant records linked to this MerchantPackage
    package_merchants = PackageMerchant.objects.filter(merchant_list=merchant)

    # Fetch all related PackageItems
    package_items = PackageItem.objects.filter(merchant_list__in=package_merchants)

    # Organize products under the same merchant
    product_data = {}
    for package_item in package_items:
        product = package_item.product_details
        if product:
            if product.id not in product_data:
                product_data[product.id] = {
                    "id": product.id,
                    "name": product.product_name or "N/A",
                    "description": product.product_description or "No description available",
                    "image": product.product_image.url if product.product_image else "",
                    "pricing": [],
                    "total_adult_price": 0,
                    "total_children_price": 0,
                    "grand_total_price": 0
                }

            # Add pricing details
            product_data[product.id]["pricing"].append({
                "category": "Adult",
                "selling_price": package_item.adult_selling_price or 0,
                "agent_price": package_item.adult_agent_price or 0,
                "commission_price": package_item.adult_commission_price or 0,
                "commission_percent": package_item.adult_commission_percent or 0,
                "number": package_item.adult_number or 0,
                "total_price": (package_item.adult_selling_price or 0) * (package_item.adult_number or 0)
            })
            product_data[product.id]["pricing"].append({
                "category": "Children",
                "selling_price": package_item.children_selling_price or 0,
                "agent_price": package_item.children_agent_price or 0,
                "commission_price": package_item.children_commission_price or 0,
                "commission_percent": package_item.children_commission_percent or 0,
                "number": package_item.children_number or 0,
                "total_price": (package_item.children_selling_price or 0) * (package_item.children_number or 0)
            })

            # Sum up prices
            product_data[product.id]["total_adult_price"] += package_item.total_adult_price or 0
            product_data[product.id]["total_children_price"] += package_item.total_children_price or 0
            product_data[product.id]["grand_total_price"] += package_item.grand_total_price or 0

    # Merchant data
    merchant_data = {
        "merchant_id": merchant.id,
        "merchant_name": merchant.merchant,
        "merchant_code": package_merchants.first().merchant_code if package_merchants.exists() else "N/A",
        "merchant_type": package_merchants.first().merchant_type.name if package_merchants.exists() and package_merchants.first().merchant_type else "N/A",
        "contact_person": merchant.contact_person or "N/A",
        "contact_number": merchant.contact_number or "N/A",
        "email": merchant.email or "N/A",
    }

    # Final Response
    response_data = {
        "merchant": merchant_data,
        "products": list(product_data.values())  # Convert dict to list
    }

    return JsonResponse(response_data)


def package_status_history(request, package_id):
    # Fetch the package by ID
    package = get_object_or_404(Package, id=package_id)

    # Fetch all logs related to the package, ordered by updated_at
    package_logs = PackageLog.objects.filter(package=package).order_by('-updated_at')

    # Pass package logs to the template
    return render(request, 'package_all_details.html', {
        'package_logs': package_logs,
        'package': package,
    })