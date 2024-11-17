from django.urls import path 
from django.urls import path, include

from . import views


urlpatterns = [

    # path('',views.home, name=""),
    path('',views.main, name="home"),
    # path('', views.tabs_view, name=""),

   
    

 
]