from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

 
app_name = 'user_product_app'


urlpatterns = [
    path('', product_list, name='list_products'),
    path('view/<int:id>/', product_view, name='product_view'),
    path('view/<int:id>/get_details/<int:colorId>/', collect_image, name='collect_image'),
    path('wishlist/', wishlist_management.wishlist_view, name='wishlist_view'),
    path('add_wishlist/<int:id>/', wishlist_management.add_wishlist_item, name='add_wishlist_item'),
    path('remove_wishlist_item/<int:id>/', wishlist_management.remove_from_wishlist, name='remove_from_wishlist'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)