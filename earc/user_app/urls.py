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
    path('resent_otp/', otp_resent, name='otp_resent'),
    path('404error/', fournoterror, name='fournoterror'),
    path('email/', forget_password_user_conform, name='forget_password_user_conform'),
    path('forget_otp/', sent_forget_password_otp, name='sent_forget_password_otp'),
    path('forget_password/', forget_password, name='forget_password'),
    path('change_password/', change_password, name='change_password'),
    path('account/', account_view, name='account_view'),
    path('user/', update_password, name='update_password'),
    path('details/<int:id>/', update_details, name='update_details'),
    path('address/', add_address, name='add_address'),
    path('address/<int:id>/', update_address, name='update_address'),
    path('delete_address/<int:id>/', delete_address, name='delete_address'),
    path('wallet/', wallet_view, name='wallet_view')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)