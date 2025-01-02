from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('dashboard/', views.dashboard, name='admin-dashboard'),

    # /////////////////////////////////////////////////////////////////////////////////
    path('main_page/', views.main_page, name='main_page'),
    path('main_page/edit/<int:id>/', views.main_edit, name='main_edit'),
    path('main_choice/edit/<int:id>/', views.main_choose, name='main_choice'),
    path('main_about/', views.main_about, name='main_about'),


    path('user/', views.user_list, name='user_list'),
    path('user/dashboard', views.user_dashboard, name='user_dashboard'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('roles/', views.user_roles, name='user_roles'),
    
    path('roles_permission/', views.roles_permission, name='user_roles_permission'),
    path('roles_permission/edit/<int:role_id>/', views.edit_roles_and_packages, name='edit_roles_permission'),

    # path('get-packages-by-system/<int:system_id>/', views.get_packages_by_system, name='get_packages_by_system'),

    path('roles/list', views.list_roles, name='list_roles'),
    path('roles/edit', views.edit_role, name='edit_role'),
    path('delete-role/<int:role_id>/', views.delete_role, name='delete_role'),

    
    path('permission/list', views.list_permission, name='list_permission'),
    
    # package
      path('package/', views.package_list, name='package_list'),
      path('package/dashboard', views.package_dashboard, name='package_dashboard'),
    # ////////////////////////////////////////////////////////////////////////////

   path('merchant/dashboard', views.merhotel_dashboard, name='merhotel_dashboard'),

    path('hotel/', views.hotel_list, name='hotel_list'),

    # hotel type
    path('hotel/type', views.hotel_type, name='hotel_type'),
    path('hotel/edit', views.hotel_type_edit, name='hotel_type_edit'),
    path('hotel/delete/<int:hotel_type_id>/', views.hotel_type_delete, name='hotel_type_delete'),  # Note the trailing slash
    path('hotel/add/', views.hotel_type_add, name='hotel_type_add'),

    # hotel facilities
    path('hotel/facilities/', views.hotel_facilities, name='hotel_facilities'),
    path('hotel/facilities/add/', views.hotel_facility_add, name='hotel_facility_add'),
    path('hotel/facilities/edit/', views.hotel_facility_edit, name='hotel_facility_edit'),
    path('hotel/facilities/delete/<int:facility_id>/', views.hotel_facility_delete, name='hotel_facility_delete'),

    # room hotel
    path('room/', views.hotel_room, name='room_type'),
    path('room/add/', views.room_type_add, name='room_type_add'),  # This is the add view
    path('room/edit', views.room_type_edit, name='room_type_edit'),
    path('room/delete/<int:room_type_id>/', views.room_type_delete, name='room_type_delete'),  # Note the trailing slash

    # room facilities
    path('room/facilities', views.hotel_room_faci, name='hotel_room_faci'),
    path('room/facilities/add/', views.room_facility_add, name='room_facility_add'),
    path('room/facilities/edit/', views.room_facility_edit, name='room_facility_edit'),
    path('room/facilities/delete/<int:facility_id>/', views.room_facility_delete, name='room_facility_delete'),
    
    # hotel view
    path('hotel/view', views.hotel_view, name='hotel_view'),
    path('hotel/view/add/', views.view_add, name='view_add'),
    path('hotel/view/edit/', views.view_edit, name='view_edit'),
    path('hotel/view/delete/<int:view_id>/', views.view_delete, name='view_delete'),


    # bed room
    path('room/bed', views.room_bed, name='room_bed'),
    path('room/bed/add/', views.bed_add, name='bed_add'),
    path('room/bed/edit/', views.bed_edit, name='bed_edit'),
    path('room/bed/delete/<int:bed_id>/', views.bed_delete, name='bed_delete'),

    path('news/', views.news, name='news'),
    path('news/add', views.news_add, name='news_add'),
    path('review/', views.review, name='review'),
    # /////////////////////////////////////////////////////////////////////////////

    path('sales/dashboard', views.sales_dashboard, name='sales_dashboard'),
    # ////////////////////////////////////////////
   

]