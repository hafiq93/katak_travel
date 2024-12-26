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

def admin_required(user):
    return user.is_superuser or user.is_staff

@user_passes_test(admin_required, login_url='/login/')
def analytics_dashboard(request):
    analytics_data = WebsiteAnalytics.objects.filter(page_url__icontains='/home').order_by('-timestamp') # Get all data sorted by timestamp
    total_visits = analytics_data.count()
    return render(request, 'analytics_dashboard.html', {'data': analytics_data, 'total_visits': total_visits})
    