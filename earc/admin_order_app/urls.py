from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'admin_order_app'

urlpatterns = [
    path('', order_list, name='order_list'),
    path('update_status/', update_status, name='update_status'),
    path('details/<int:id>/', order_details, name='order_details')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)