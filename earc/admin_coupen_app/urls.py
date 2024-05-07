from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'admin_coupen_app'

urlpatterns = [
    path('', list_coupens, name='list_coupens'),
    path('add/', add_coupen, name='add_coupen'),
    path('update/<int:id>/', update_coupen, name='update_coupen'),
    path('block_unblock/<int:id>/', block_and_unblock, name='block_unblock'),
    path('expiry/<int:id>/', expire_coupen, name='expire_coupen'),
    path('coupen_details/<int:id>/', coupen_details, name='coupen_details'),
    path('delete/<int:id>/', delete_coupen, name='delete_coupen')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)