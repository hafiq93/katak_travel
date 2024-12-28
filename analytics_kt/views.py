from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .models import WebsiteAnalytics
from user_kt.models import User,Profile
from page.models import MainPage,MainChoose,AboutUs,ContactUs
from admin_kt.models import Permission,Roles,UserRole, RolePermission
import re
from django.db.models import Q # Import the User model from user_kt app
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

def admin_required(user):
    return user.is_superuser or user.is_staff

@user_passes_test(admin_required, login_url='/login/')
def analytics_dashboard(request):
    # Default to show all data
    start_date = None
    end_date = None

    # Get the filter parameters from the GET request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # If both dates are provided, parse them and filter the data
    if start_date_str and end_date_str:
        try:
            # Parse the provided date strings into datetime objects
            start_date = parse_datetime(start_date_str)
            end_date = parse_datetime(end_date_str)
        except ValueError:
            pass  # Handle invalid date formats if needed

    # Build the filter conditions
    url_filter = Q(page_url__icontains='/home') & (
        Q(page_url__icontains='kataktravel.com')  # This matches both 'www.kataktravel.com' and 'kataktravel.com'
    )

    # Filter analytics data by date range (if provided)
    if start_date and end_date:
        # Filter by page URL (both www and non-www) and date range
        analytics_data = WebsiteAnalytics.objects.filter(
            url_filter,
            timestamp__range=(start_date, end_date)  # Date range filter
        ).order_by('-timestamp')
    else:
        # If no date filter is provided, only filter by the URL
        analytics_data = WebsiteAnalytics.objects.filter(url_filter).order_by('-timestamp')

    # Get the total number of visits
    total_visits = analytics_data.count()

    # Return the filtered data to the template
    return render(request, 'analytics_dashboard.html', {'data': analytics_data, 'total_visits': total_visits})