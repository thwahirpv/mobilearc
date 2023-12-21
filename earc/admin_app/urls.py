from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

 
app_name = 'admin_app'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)