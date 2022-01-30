from django.contrib import messages
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User, Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import RegForm
from .models import CATEGORIES, Clothe, Customer, Tailor
from django.core import serializers
from django.conf import settings
import json

@login_required(login_url='main/login.html')
def mail_view(request, clothe_id):
    sender = Customer.objects.get(user=request.user.id)    
    send_mail(
            'New Cloth Order',
            f'This is an order for this clothe ... by {request.user} with email address {request.user.email}\
                and phone number {sender.phone_no}, from: {sender.address}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS],
            fail_silently=False
            )
    
    return render(request, 'main/clothe.html', None)

def edit_view(request, tailor):
    tailor = int(tailor)    
    if request.method == 'POST':    
        thistailor = Tailor.objects.get(user=tailor);
        try:
            thistailor.background_image = request.FILES['background_image']
            thistailor.save()
            print(thistailor)

        except:
            thistailor.profile_image = request.FILES['profile_image']
            thistailor.save()
        return redirect(f'/main/tailorProfile/{tailor}')

@login_required(login_url='main/login.html')
def clothe_sample_view(request, clothe_id):
    object = Clothe.objects.get(id=clothe_id)
    return render(request, 'main/clothe.html', {'object': object})

def join_view(request):
    context = {
        'AnonymousUser': AnonymousUser
    }    
    return render(request, 'main/join.html', context)

def welcome_view(request):
    context = {
        'AnonymousUser': AnonymousUser
    }
    return render(request, 'main/welcome.html', context)

def home_view(request):
    if request.method == 'POST':
        query = []
        query_names = []

        n = 0
        req = list(request.POST.keys())[1:]
        while (n < len(req)):
            object = Clothe.objects.filter(category = req[n])  
            if (len(object) != 0):
                for obj in object:
                    query_names.append(obj.company_name.username)
                query.append(serializers.serialize('json', object))
            m = n + 1

            while (m < len(req)):
                object = Clothe.objects.filter(category = f'{req[n]}' f'{req[m]}')
                if (len(object) != 0):
                    for obj in object:
                        query_names.append(obj.company_name.username)
                    query.append(serializers.serialize('json', object))
                m += 1
            n += 1

        i = 0
        j = 0
        query_obj = {}
        #updated_query = []
        for obj in query:
            a = json.loads(obj)    
            for objects in a:
                objects['name'] = query_names[i]
                i += 1
            #updated_query.append(json.dumps(a))
            query_obj[j] = a
            j += 1
        
        return HttpResponse(json.dumps(query_obj))
    query_obj = Clothe.objects.all()[0:9]
    context = {
        'AnonymousUser': AnonymousUser,
        'query_obj': query_obj
    }    
    return render(request, 'main/home.html', context)

def tailor_profile_view(request, tailor):
    try:
        info = Tailor.objects.get(user=tailor)
        clothes = Clothe.objects.filter(company_name=tailor)
    except:
        return HttpResponse("This tailor does not exist")
    context = {
        'profileinfo': info,
        'AnonymousUser': AnonymousUser,
        'clothes': clothes
    }
    return render(request, 'main/profile.html', context)

def auth_view(request):
    return render(request, 'main/auth.html', None)
    
def login_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or referer[-5:] != '/auth':
        return redirect("/main/auth")
    else:
        if request.method == 'POST':    
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            try:
                if request.POST['next']:
                    next = request.POST['next']
            except UnboundLocalError:
                pass
            user = authenticate(request, username=username, password=password)
            if user is not None:    
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Login successful")
                try:
                    return redirect('/main/',next)
                except UnboundLocalError:
                    return redirect('/main')
            else:
                return HttpResponse("Test successful, but not registered")
        return render(request, 'main/login.html', None)
        
def register_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or referer[-5:] != '/auth':
        return redirect("/main/auth")
    else:
        if request.method == "POST":
            form = RegForm(request.POST)    
            if form.is_valid():
                form.save()
                group = Group.objects.get(name='Customers')
                group.user_set.add(User.objects.get(username = request.POST['username']))
                messages.add_message(request, messages.SUCCESS, "Registration successful")
                return HttpResponse("Test successful")
            messages.add_message(request, messages.ERROR, f"{form.errors}")
            return HttpResponse(f"Test successful, but unable to register user {form.errors}")
        form = RegForm()
        return render(request, 'main/register.html', {'register_form': form})
    
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logged Out")
    return redirect("/main", permanent=True)