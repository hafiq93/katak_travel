# package_kt/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get-packages/<int:system_id>/', views.get_packages, name='get_packages'),
    path('get-subpackages/<int:package_id>/',  views.get_subpackages, name='get_subpackages'),
    path('get-subpackage-2/<int:subpackage_id>/', views.get_subpackage_2, name='get_subpackage_2'),
]   