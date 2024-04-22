from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'cart_app'

urlpatterns = [
   path('', cart_management.view_cart, name='view_cart'),
   path('add/', cart_management.add_cart, name='add_item_to_cart'),
   path('remove/<int:id>/', cart_management.remove_item, name='remove_item'),
   path('update_quantity/', cart_management.update_quantity, name='update_quantity'),
   path('update_subtotal/', cart_management.update_subtotal, name='update_subtotal'),
   path('clear/', cart_management.clear_cart, name='clear_cart')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
