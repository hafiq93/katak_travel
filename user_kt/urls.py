from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),  # Example login path
    # path('register/', views.user_register, name='register'),  # Example register path
    path('profile/', views.user_profile, name='profile'),  # Example register path
    path('profile/edit', views.edit_profile, name='edit_profile'),  # Example register path
    path('setting_profile/', views.setting_profile, name='setting_profile'),
    path('logout/', views.logout_view, name='logout'),  # Example register path
    
]