from django.urls import path
from . import views
urlpatterns = [
    # Define your URL patterns here
    path('add/', views.pack_list_add, name='pack_list_add'),  # Separate URL for adding a new package
    path('add/<int:id>/', views.pack_list_add, name='pack_list_add'),  # Capture the id in the URL

    path('upload_main_image/<int:package_id>/',views.upload_main_images, name="upload_main_image"),
    path('upload_other_images/<int:package_id>/', views.upload_other_images, name='upload_other_images'),
    path('delete-main-image/<int:image_id>/', views.delete_main_image, name='delete_main_image'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),


    path('add/items/<int:package_id>/', views.pack_list_add_items, name='pack_list_add_items'),
    path('form/<int:id>/', views.pack_merchant, name='pack_merchant'),
    path('product-pricing/', views.product_pricing_view, name='product_pricing'),

    path('delete_merchant/<int:id>/', views.delete_merchant, name='delete_merchant'),
    path('get_merchant/<int:id>/', views.get_merchant, name='get_merchant'),

    path('add/page_3/edit/<int:merchant_id>/', views.pack_mer_edit, name='pack_mer_edit'),

    path('list/<int:package_id>/', views.pack_price, name='pack_price'),

    path('merchant/delete/<int:id>/', views.delete_merchant_new, name='delete_merchant_new'),
    path('merchant/duplicate/<int:id>/', views.duplicate_merchant, name='duplicate_merchant'),

    path('merchant-details/<int:id>/', views.get_merchant_details, name='merchant-details'),
    
    path('details/<int:merchant_id>/', views.pack_form, name='pack_form'),  # For editing merchant
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('form/product/<int:product_id>/', views.add_price, name='add_price'),

    path('details/product/<int:product_id>/', views.products_details, name='products_details'),

    path('add_product/<int:product_id>/', views.add_product, name='add_product'),

    path('details/all/<int:package_id>/', views.package_all_details, name='package_all_details'),
    
    path('get-product-details/<int:product_id>/', views.get_product_details, name='get_product_details'),

    path('api/merchant/<int:merchant_id>/', views.get_merchant_product_details, name='merchant-details'),

    path('<int:package_id>/update-status/', views.update_package_status, name='update_package_status'),
    path('<int:package_id>/history/', views.package_status_history, name='package_status_history'),
    path('send-back/<int:package_id>/', views.send_back, name='send_back'),
    path('package/publish/<int:package_id>/', views.publish_package, name='publish_package'),   

    
    
   
]