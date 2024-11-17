from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import User, Profile
from django.contrib.auth.hashers import make_password

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Email: {email}, Password: {password}")  # Debug print
        user = authenticate(request, username=email, password=password)

        if user is not None:
            print(f"User found: {user}")  # Debug print
            if user.is_superuser or user.is_staff:
                auth_login(request, user)  # Log in admin or staff user
                return redirect('admin-dashboard')  # Redirect to admin dashboard
            else:
                # Non-admin users get logged in and redirected to homepage
                auth_login(request, user)
                return redirect('home')  # Redirect to homepage
        else:
            print("Authentication failed")  # Debug print
            messages.error(request, "Invalid credentials.")  # Show error message
    
    return render(request, 'user_kt/login.html')  # Your login template

def user_register(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        identity_type = request.POST.get('identity_type')
        identity_no = request.POST.get('identity_no')

        # Check if password and confirm password match and enforce minimum length
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'user_kt/register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'user_kt/register.html')

        # Check if the email already exists
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, 'Email is already taken.')
        #     return render(request, 'user_kt/register.html')

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)  # Hash the password before saving
        )

        # Create the user profile
        # Profile.objects.create(
        #     user=user,
        #     identity_type=identity_type,
        #     identity_no=identity_no,
        #     country=country
        # )

        # Authenticate and log the user in
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page or another page after registration

        return redirect('login')  # Redirect to login if authentication fails

    return render(request, 'user_kt/register.html')

@login_required
def user_profile(request):
    # Get the logged-in user's profile
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'user_kt/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    # Get the logged-in user's profile
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'user_kt/edit_profile.html', {'profile': profile})

@login_required
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the main page

@login_required
def setting_profile(request):
    # Get the logged-in user's profile
   
    return render(request, 'user_kt/setting_profile.html')
