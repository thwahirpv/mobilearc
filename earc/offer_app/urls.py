from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'admin_offer_app'

urlpatterns = [
    path('category/', list_category, name='list_category'),
    path('category/add/', add_category_offer, name='add_category_offer'),
    path('category/block_unblock/<int:id>/', block_unblock_category, name='block_unblock_category'),
    path('category/update/<int:id>/', update_category_offer, name='update_category_offer')

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)