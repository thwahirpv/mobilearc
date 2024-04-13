from django.http import JsonResponse
from django.shortcuts import redirect, render
from admin_product_app.models import category, brands, products, Colors, Images, Storage
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q



    
