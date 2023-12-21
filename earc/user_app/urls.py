from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

 
app_name = 'user_app'

urlpatterns = [
    path('register/', user_registraion, name='user_registraion'),
    path('otp/', user_otp, name='user_otp'),
    path('login/', user_login, name='user_login'),
    path('home/', user_home, name='user_home'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)