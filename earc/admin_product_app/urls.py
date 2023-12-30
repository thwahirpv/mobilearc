from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . views import *

 
app_name = 'admin_product_app'

urlpatterns = [
    # ===============Products========================
    path('', product_management.list_products, name='list_products'),
    path('add/', product_management.add_product, name='add_product'),
    path('edit/<int:id>', product_management.update_product, name='update_product'),

    # ==============Brands=======================
    path('brands/', brand_management.brands, name='list_brands'),
    path('brands/add/', brand_management.add_brand, name='add_brand'),

    # ==========Category=================
    path('category/', category_management.category, name='admin_category'),
    path('<int:id>/', category_management.delete_category, name='delete_category'),
    path('category/<int:id>/', category_management.update_category, name='update_category'),
    path('category/<str:action>/<int:id>/', category_management.block_and_unblock, name='block_and_unblock'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)