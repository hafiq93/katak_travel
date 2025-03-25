from django.urls import path 
from django.urls import path, include

from . import views


urlpatterns = [

    # path('',views.home, name=""),
    path('packages',views.main_package, name="main_packages"),
    # path('', views.tabs_view, name=""),

   
    

 
]