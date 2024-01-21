from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . views import *

 
app_name = 'admin_product_app'

urlpatterns = [
    # ===============Products========================
    path('list/', product_management.list_products, name='list_products'),
    path('add/', product_management.add_product, name='add_product'),
    path('add/getbrands/<str:brand_name>/', get_category, name='get_category_product_adding'),   
    path('edit/<int:id>/', product_management.update_product, name='update_product'),
    path('edit/<int:id>/get_category/<str:brand_name>/', get_category, name='get_category'),
    path('block/<str:action>/<int:id>/', product_management.block_and_unblock, name='product_block_and_unblock'),   

    # ==============Brands=======================
    path('brands/', brand_management.brands, name='list_brands'),
    path('brands/add/', brand_management.add_brand, name='add_brand'),
    path('brand/<int:id>', brand_management.update_brand, name='update_brand'),
    path('brand/del/<int:id>/', brand_management.delete_brand, name='delete_brand'),
    path('brand/<str:action>/<int:id>/', brand_management.block_and_unblock, name='brand_block_and_unblock'),

    # ==========Category=================
    path('category/', category_management.category, name='admin_category'),
    path('<int:id>/', category_management.delete_category, name='delete_category'),
    path('category/<int:id>/', category_management.update_category, name='update_category'),
    path('category/<str:action>/<int:id>/', category_management.block_and_unblock, name='category_block_and_unblock'),

    # ==========variants=========================
    path('variants/', variant_management.list_variants,  name='list_variants'),
    path('variant/add/', variant_management.add_variant, name='add_variant'),
    path('variant/add/getcandb/<str:product_name>/', get_brand_and_category, name='get_brand_and_category_variant_adding'),
    path('variant/edit/<int:id>/', variant_management.update_variant, name='update_variant'),
    path('variant/edit/<int:id>/getband&category/<str:product_name>/', get_brand_and_category, name='get_brand_and_category_variant_updating'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)