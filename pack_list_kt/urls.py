from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('add/page_1/', views.pack_list_add, name='pack_list_add'),  # Separate URL for adding a new package
    path('add/page_1/<int:id>/', views.pack_list_add, name='pack_list_add'),  # Capture the id in the URL
    path('add/items/<int:package_id>/', views.pack_list_add_items, name='pack_list_add_items'),
    path('add/page_2/<int:id>/', views.pack_merchant, name='pack_merchant'),
   
]