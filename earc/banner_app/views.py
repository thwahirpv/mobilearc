from django.shortcuts import get_object_or_404, redirect, render
from .models import Banner
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.urls import reverse
from .models import priority_choices
from django.db.models import Q



def list_banner(request):
    if not request.user.is_authenticated:
        return redirect('admin_app:admin_login')
    
    # first_banner = Banner.objects.filter(Q(banner_active=True) & Q(banner_type='first_banner'))
    # secondary_banner = Banner.objects.filter(Q(banner_active=True) & Q(banner_type='secondary_banner'))
    context = {
        'banners_items':Banner.objects.all()
    }
    return render(request, 'admin_template/list_banner.html', context)


def add_banner(request):
    if not request.user.is_authenticated:
        return redirect('admin_app:admin_login')
    
    if request.method == 'POST':
        banner_title = request.POST.get('banner_title')
        banner_image = request.FILES.get('banner_image')
        priority = request.POST.get('priority')
        banner_text = request.POST.get('banner_text', None)
        banner_type = request.POST.get('banner_type')

        url = reverse('banner_app:add_banner')

        if banner_image:
            try:
                file_content = banner_image.read()
                img = Image.open(BytesIO(file_content))
                if not img.format.lower() in ['jpg', 'jpeg', 'png']:
                    messages.error(request, 'Upload jpg or jpeg')
                    return redirect(url)
            except:
                messages.error(request, 'Invalid file!')
                return redirect(url)
        else:
            messages.error(request, 'Upload image!')
            return redirect(url)


        if not type(banner_title) == str:
            messages.error(request, 'Enter valid title!')
            return redirect(url)
        elif priority == '':
            messages.error(request, 'Select priority!')
        elif banner_text is not None:
            if not type(banner_text) == str:
                messages.error(request, 'Enter valid Discription!')
                return redirect(url)
            
        Banner.objects.create(banner_title=banner_title, banner_image=banner_image, priority=priority, banner_text=banner_text, banner_type=banner_type)
        return redirect('banner_app:list_banner') 
    context = {
        'priority':priority_choices.choices,
        'banner_type': Banner.BANNER_TYPE_CHOICES
        }
    return render(request, 'admin_template/add_banner.html', context)
    


def banner_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_app:admin_login')
    
    url  = reverse('banner_app:edit_banner', kwargs={'id':id}) 
    banner_obj = get_object_or_404(Banner, banner_id=id)

    if request.method == 'POST':
        banner_title = request.POST.get('banner_title', banner_obj.banner_title)
        banner_image = request.FILES.get('banner_image', banner_obj.banner_image)
        priority = request.POST.get('priority', banner_obj.priority)
        banner_text = request.POST.get('banner_text', banner_obj.banner_text)
        banner_type = request.POST.get('banner_type', banner_obj.banner_type)
        

        if banner_image:
            try:
                file_content = banner_image.read()
                img = Image.open(BytesIO(file_content))
                if not img.format.lower() in ['jpg', 'jpeg', 'png']:
                    messages.error(request, 'Upload jpg or jpeg')
                    return redirect(url)
            except:
                messages.error(request, 'Invalid file!')
                return redirect(url)

        if banner_title is not None:
            if not type(banner_title) == str:
                messages.error(request, 'Enter valid title!')
                return redirect(url)
        elif priority == '':
            messages.error(request, 'Select priority!')
            return redirect(url)
        elif banner_text is not None:
            if banner_text.isalpha():
                messages.error(request, 'Enter valid text!')
                return redirect(url)
            
        banner_obj.banner_title = banner_title
        banner_obj.banner_image = banner_image
        banner_obj.priority = priority
        banner_obj.banner_text = banner_text
        banner_obj.banner_type = banner_type
        banner_obj.save()
        return redirect('banner_app:list_banner')
    context = {
        'banner_obj':banner_obj,
        'priority':priority_choices.choices,
        'banner_type':Banner.BANNER_TYPE_CHOICES
        }
    return render(request, 'admin_template/add_banner.html', context)


def block_and_unblock(request, action, id):
    if not request.user.is_authenticated:
        return redirect('admin_app:admin_login')
    
    banner_obj = get_object_or_404(Banner, banner_id=id)
    
    if action == 'get_name':
        context = {
            'status':'success',
            'title': banner_obj.banner_title, 
        }
        return JsonResponse(context, safe=True)
    elif action == 'block':
        banner_obj.banner_active = False
        banner_obj.save()
        context = {
            'status': 'success',
            'title': 'Blocked',
            'text': f'{banner_obj.banner_title} id Blocked'
        }
        return JsonResponse(context, safe=True)
    elif action == 'unblock':
        banner_obj.banner_active = True
        banner_obj.save()
        context = {
            'status': 'success',
            'title': 'Unblocked', 
            'text': f'{banner_obj.banner_title} is Unblocked'
        }
        return JsonResponse(context, safe=True)


def delete_banner(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_app:admin_login')
    banner_obj = get_object_or_404(Banner, banner_id=id)
    banner_obj.delete()
    return redirect('banner_app:list_banner')

