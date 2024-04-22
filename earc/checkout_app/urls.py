from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'checkout_app'

urlpatterns = [
    path('', checkout, name='checkout')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)