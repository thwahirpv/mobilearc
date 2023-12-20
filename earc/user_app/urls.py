from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

 
app_name = 'user_app'

urlpatterns = [
    path('home/', views.user_home, name='user_home')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)