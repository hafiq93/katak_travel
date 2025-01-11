from django.urls import path
from . import views  # Ensure views are imported if used

urlpatterns = [
    path('', views.merchant_home, name='admin_home'),  # Example view
]