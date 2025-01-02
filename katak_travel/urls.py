"""
URL configuration for katak_travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect 

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('home_page', permanent=True)),
    path("__reload__/", include("django_browser_reload.urls")),
    # path('admin/', admin.site.urls),
    path('', include('page.urls')),
    path('admin/', include('admin_kt.urls')),
    path('hms/', include('hms_kt.urls')),
    path('merchant/', include('merchant_kt.urls')),
    path('', include('main_kt.urls')),
    path('', include('user_kt.urls')),
    path('', include('hote_kt.urls')),
    path('api/', include('package_kt.urls')),  # Include the API URLs
    path('analytics/', include('analytics_kt.urls')),
    # path("hotel/", include("hote_kt.urls")),
    # path("katak_travel/", include("main_kt.urls")),
    # path("merchant/", include("merchant_kt.urls")),
    # path("profile/", include("user_kt.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
