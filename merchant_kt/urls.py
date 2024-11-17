from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('dashboard/', views.dashboard, name='merchant-dashboard'),
    # path('hotel/', views.hotel_list, name='hms-list'),
]