from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'admin_offer_app'

urlpatterns = [
    # Category offers
    path('category/', list_category, name='list_category'),
    path('category/add/', add_category_offer, name='add_category_offer'),
    path('category/block_unblock/<int:id>/', block_unblock_category, name='block_unblock_category'),
    path('category/update/<int:id>/', update_category_offer, name='update_category_offer'),
    path('category/details/<int:id>/', category_offer_details, name='category_offer_details'),

    # Brand offers
    path('brand/', list_brand, name='list_brand'),
    path('brand/add/', add_brand_offer, name='add_brand_offer'),
    path('brand/block_unblock/<int:id>/', block_and_unblock_brand, name='block_and_unblock_brand'),
    path('brand/update/<int:id>/', update_brand_offer, name='update_brand_offer'),
    path('brand/details/<int:id>/', brand_details, name='brand_details')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)