from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'banner_app'

urlpatterns = [
    path('', list_banner, name='list_banner'),
    path('add/', add_banner, name='add_banner'),
    path('edit/<int:id>/', banner_edit, name='edit_banner' ), 
    path('delete/<int:id>/', delete_banner, name='delete_banner'),
    path('<str:action>/<int:id>/', block_and_unblock, name='block_and_unblock'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)