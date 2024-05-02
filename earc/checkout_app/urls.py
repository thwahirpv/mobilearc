from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'checkout_app'

urlpatterns = [
    path('', checkout, name='checkout'),
    path('place_order/', place_order, name='place_order'),
    path('history/', order_history, name='order_history'),
    path('details/<int:id>/', order_details, name='order_details'),
    path('cancel/<str:action>/<int:id>/', cancel_order, name='cancel_order'),
    path('rate/', rate_review, name='rate_review'),
    path('placed/', order_placed, name='order_placed')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)