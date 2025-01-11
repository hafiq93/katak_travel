from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', include('data_api_kt.admin_kt.urls')),
    path('merchant/', include('data_api_kt.merchant_kt.urls')),
]