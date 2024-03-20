from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

 
app_name = 'admin_product_app'

urlpatterns = [
    # ===============Products========================
    path('list/', product_management.list_products, name='list_products'),
    path('add/', product_management.add_product, name='add_product'),
    path('add/getbrands/<str:brand_name>/', get_category, name='get_category_product_adding'),   
    path('edit/<int:id>/', product_management.update_product, name='update_product'),
    path('delete_product/<int:id>/', product_management.delete_product, name='delete_product'),
    path('edit/<int:id>/get_category/<str:brand_name>/', get_category, name='get_category'),
    path('<str:action>/<int:id>/', product_management.block_and_unblock, name='product_block_and_unblock'),   

    # ==============Brands=======================
    path('brands/', brand_management.brands, name='list_brands'),
    path('brands/add/', brand_management.add_brand, name='add_brand'),
    path('brands/<str:action>/<int:id>/', brand_management.block_and_unblock, name='brand_block_and_unblock'),
    path('brand/<int:id>', brand_management.update_brand, name='update_brand'),
    path('brand/del/<int:id>/', brand_management.delete_brand, name='delete_brand'),

    # ==========Category=================
    path('category/', category_management.category, name='admin_category'),
    path('<int:id>/', category_management.delete_category, name='delete_category'),
    path('category/<int:id>/', category_management.update_category, name='update_category'),
    path('category/<str:action>/<int:id>/', category_management.block_and_unblock, name='category_block_and_unblock'),

    # ============Variations==============
    path('variants/<int:id>/', variant_management.list_variant, name='list_variant'),
    path('variant/<int:id>/', variant_management.add_color_variant, name='add_variant'),
    path('varinat/<int:product_id>/<int:id>/', variant_management.add_storage_variant, name='add_storage_variant'),
    path('view/<int:id>/', variant_management.variant_detailed_view, name='variant_detailed_view'),
    path('delete_image/<int:image_id>/<int:id>/', variant_management.delete_image, name='delete_image'),
    path('change_image/<int:image_id>/<int:id>/', variant_management.change_image, name='change_image'),
    path('delete_variant/<int:product_id>/<int:id>/', variant_management.delete_color, name='delete_color')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)