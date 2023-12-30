from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

 
app_name = 'admin_app'

urlpatterns = [
    # =============Login and Logout===============
    path('login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    # =============Login and Logout===============

    # ==============Dashboard=====================
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    # =============Dashboard=======================

    # ==============Crud oprations=======================
    path('users/', user_crud_view.load_table, name='load_table'),
    path('user/create', user_crud_view.create_user, name='create_user'),
    path('user/<int:id>/update', user_crud_view.update_user, name='update_user'),
    path('user/<int:id>/delete', user_crud_view.delete, name='delete_user'),
    path('user/<int:id>/block', user_crud_view.block_user, name='block_user'),
    path('user/<int:id>/unblock', user_crud_view.unblock_user, name='unblock_user'),
    # ==============Crud oprations=======================

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)