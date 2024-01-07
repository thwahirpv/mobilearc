from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

 
app_name = 'user_app'

urlpatterns = [
    path('', user_home, name='user_home'),
    path('register/', user_registration , name='user_registration'),
    path('otp/', otp_checking, name='otp_checking'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('404error/', fournoterror, name='fournoterror')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)