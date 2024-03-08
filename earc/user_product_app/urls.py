from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

 
app_name = 'user_product_app'


urlpatterns = [
    path('', product_list, name='list_products'),
    path('view/<int:id>/', product_view, name='product_view'),
    path('view/<int:id>/get_image/<int:colorId>/', collect_image, name='collect_image'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)