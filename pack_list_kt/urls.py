from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('add/', views.pack_list_add, name='pack_list_add'),  # Separate URL for adding a new package
    path('add/<int:id>/', views.pack_list_add, name='pack_list_add'),  # Capture the id in the URL
    path('add/items/<int:package_id>/', views.pack_list_add_items, name='pack_list_add_items'),
    path('form/<int:id>/', views.pack_merchant, name='pack_merchant'),

    path('delete_merchant/<int:id>/', views.delete_merchant, name='delete_merchant'),
    path('get_merchant/<int:id>/', views.get_merchant, name='get_merchant'),

    path('add/page_3/edit/<int:merchant_id>/', views.pack_mer_edit, name='pack_mer_edit'),

    path('list/<int:package_id>/', views.pack_price, name='pack_price'),
    path('merchant-details/<int:id>/', views.get_merchant_details, name='merchant-details'),
    path('details/<int:merchant_id>/', views.pack_form, name='pack_form'),  # For editing merchant

    path('add_price/<int:product_id>/', views.add_price, name='add_price'),
   
]