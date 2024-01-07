from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . views import *

 
app_name = 'admin_product_app'

urlpatterns = [
    # ===============Products========================
    path('list/', product_management.list_products, name='list_products'),
    path('add/', product_management.add_product, name='add_product'),
    path('add/getbrands/<str:category_name>/', product_management.get_brands, name='get_brands'),   
    path('edit/<int:id>', product_management.update_product, name='update_product'),

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
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)