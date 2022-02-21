from django.contrib import messages
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User, Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import RegForm
from .models import CATEGORIES, Clothe, Customer, Tailor, Address
from django.core import serializers
from django.conf import settings
import json
import re

from django.utils.datastructures import MultiValueDictKeyError

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




# tailor profile section
@login_required(login_url='main/login.html')
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
    return render(request, 'main/tailorprofile.html', context)

@login_required(login_url='main/login.html')
def edit_tailor_view(request, tailor):
    tailor = int(tailor)    
    if request.method == 'POST':    
        thistailor = Tailor.objects.get(user=tailor);
        try:
            thistailor.background_image = request.FILES['background_image']
            thistailor.save()
        except:
            thistailor.profile_image = request.FILES['profile_image']
            thistailor.save()
        return redirect(f'/main/tailorProfile/{tailor}')




# customer profile section
@login_required(login_url='main/login.html')
def customer_profile_view(request, customer):    
    user = User.objects.get(id=customer)
    customer = Customer.objects.get(user=user)
    try:
        default_address = Address.objects.get(user=request.user.id, default=True)
    except:
        default_address = None
    userdetails = {
        'username': user.username,
        'email': user.email,
        'phone_no1': customer.phone_no1,
        'phone_no2': customer.phone_no2,
        'this_address': default_address
    }    
    details = request.GET
    try:    
        section = details.get('section')
        if section == 'account':
            view = details.get('view')
            if view == 'overview':
                return render(request, 'main/cprofile/account.html', {'userdetails': userdetails})
            elif view == 'accountdetails':
                return render(request, 'main/cprofile/accountdetails.html', {'userdetails': userdetails})
            elif view == 'addressbook':
                addresses = Address.objects.filter(user=request.user)
                userdetails['addresses'] = addresses
                return render(request, 'main/cprofile/addressbook.html', {'userdetails': userdetails})
            elif view == 'defaultaddress':
                return render(request, 'main/cprofile/addressdetail.html', {'userdetails': userdetails})
            elif view == 'newaddress':
                return render(request, 'main/cprofile/addressoutline.html', None)
            elif view == 'addressedit':
                address_id = int(details['id'])
                try:
                    if details.get('action') == 'delete':
                        Address.objects.get(id=address_id).delete()
                        addresses = Address.objects.filter(user=request.user)
                        userdetails['addresses'] = addresses
                        return render(request, 'main/cprofile/addressbook.html', {'userdetails': userdetails})
                except:
                    pass    
                userdetails['this_address'] = Address.objects.get(id=address_id)
                return render(request, 'main/cprofile/addressdetail.html', {'userdetails': userdetails})
            elif view == 'inbox':
                return render(request, 'main/cprofile/inbox.html', {'userdetails': userdetails})
            elif view == 'payment':
                return render(request, 'main/cprofile/payment.html', {'userdetails': userdetails})

        if section == 'inbox':
            return render(request, 'main/cprofile/inbox.html', None)
        if section == 'payment':
            return render(request, 'main/cprofile/payment.html', None)
        if section == 'orders':
            return render(request, 'main/cprofile/orders.html', None)
    except Exception as e:
        return render(request, 'main/cprofile/account.html', None)
    return render(request, 'main/custprofile.html', {'userdetails': userdetails})

@login_required(login_url='main/login.html')
def edit_customer_view(request):
    if request.method == "POST":
        details = request.POST
        thiscustomer = Customer.objects.get(user=request.user.id)
        thisuser = User.objects.get(id=request.user.id)
        
        # update email if present
        if len(details.get('email', '#')) > 1:
            thisuser.email = details.get('email')

        # update rest of customer's data
        if len(details.get('phone_no1', '#')) > 1:
            thiscustomer.phone_no1 = details.get('phone_no1')
        if len(details.get('phone_no2', '#')) > 1:
            thiscustomer.phone_no2 = details.get('phone_no2')
                
        thisuser.save()
        thiscustomer.save()
        return redirect(f'/main/profile/{request.user.id}')
    return render(request, 'main/custprofile.html', None)

@login_required(login_url='main/login.html')
def newaddress_view(request):
    if request.method == "POST":
        newaddress = Address()
        newaddress.user = request.user
        newaddress.address = request.POST["address"]
        newaddress.city = request.POST["city"]
        newaddress.state = request.POST["state"]
        newaddress.zipcode = request.POST["zipcode"]
        try:
            if len(Address.objects.get(user=request.user))==1:
                newaddress.default = True
        except:
            newaddress.default = True    
        newaddress.save()
    return redirect(f'/main/profile/{request.user.id}')

@login_required(login_url='main/login.html')
def edit_address_view(request, address_id):
    this_address = Address.objects.get(id=address_id)
    if request.method == "POST":
        details = request.POST    
        if len(details.get('address', '#')) > 1:
            this_address.address = details.get('address')
        if len(details.get('city', '#')) > 1:
            this_address.city = details.get('city')
        if len(details.get('state', '#')) > 1:
            this_address.state = details.get('state')
        if len(details.get('zipcode', '#')) > 1:
            this_address.zipcode = details.get('zipcode')
        this_address.save()
    return redirect(f'/main/profile/{request.user.id}')

@login_required(login_url='main/login.html')
def change_address_view(request, address_id):
    try:    
        default_address = Address.objects.filter(user=request.user, default=True)[0]
        default_address.default = False
        default_address.save()
    except:
        pass
    this_address = Address.objects.get(user=request.user, id=address_id)
    this_address.default = True
    this_address.save()
    return redirect(f'/main/profile/{request.user.id}')



# measurements
@login_required(login_url='main/login.html')
def measureopt_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
        return redirect("/main/auth")
    else:
        if request.method == "POST":    
            option = request.POST['measureopt']
            if option == 'opt4':
                return redirect(f"/main/profile/{request.user.id}", permanent=True)
            else:
                return redirect(f"/main/auth?thisform={option}")
    return render(request, 'main/measureopt.html', None)

@login_required(login_url='main/login.html')
def measuredetails_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
        return redirect("/main/auth")    
    return render(request, 'main/measure/measuredetails.html', None)

@login_required(login_url='main/login.html')
def measurehowto_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
        return redirect("/main/auth")
    if request.method == "POST":
        option = request.POST['measureopt']
        if option is None or option == "":
            messages.add_message(request, messages.error, "Please select an option")    
            return redirect("/main/measurehowto", permanent=True)
        if option == 'opt4':
            return redirect("/main/profile", permanent=True)
        else:
            return redirect(f"/main/auth?thisform={option}")
    return render(request, 'main/measure/howtoselfmeasure.html', None)

@login_required(login_url='main/login.html')
def promeasure_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
        return redirect("/main/auth")
    if request.method == "POST":
        details = request.POST    
        customer = Customer.objects.get(user=request.user)
        newaddress = Address()
        newaddress.user = request.user
        newaddress.address = details.get('address')
        newaddress.city = details.get('city')
        newaddress.state = details.get('state')
        newaddress.zipcode = details.get('zipcode')
        newaddress.default = True
        customer.phone_no1 = details.get('phone_no1')

        customer.save()
        newaddress.save()
        return redirect(f'/main/profile/{request.user.id}')
    return render(request, 'main/measure/requestpro.html', None)



# Shopping
def cart_view(request):
    return render(request, 'main/cart.html', None)



# Authentication
def auth_view(request):
    try:    
        form_t = request.GET
        formtype = form_t['thisform']
    except MultiValueDictKeyError:
        formtype = 'signin'
    return render(request, 'main/auth.html', {'formtype': formtype})
    
def login_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
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
                #messages.add_message(request, messages.SUCCESS, "Login successful")
                try:
                    return redirect('/main/',next)
                except UnboundLocalError:
                    return redirect('/main/')
            else:
                return HttpResponse("Test successful, but not registered")
        return render(request, 'main/login.html', None)
        
def register_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
        return redirect("/main/auth")
    else:
        if request.method == "POST":
            form = RegForm(request.POST)    
            if form.is_valid():
                form.save()
                #group = Group.objects.get(name='Customers')
                #group.user_set.add(User.objects.get(username = request.POST['username']))
                #messages.add_message(request, messages.SUCCESS, "Registration successful")
                user = authenticate(request, username=request.POST['username'], 
                                    password=request.POST['password1'])
                if user is not None:
                    newcustomer = Customer(user=user)    
                    newcustomer.save()
                    login(request, user)
                return redirect("/main/auth?thisform=measureopt")
            messages.add_message(request, messages.ERROR, f"{form.errors}")
            return redirect(f'/main/auth?thisform=signup')
        form = RegForm()
        return render(request, 'main/register.html', {'register_form': form})

@login_required(login_url='main/login.html')
def change_user_pass(request):
    user = User.objects.get(id=request.user.id)
    user.password1 = request.POST['password1']
    user.password2 = request.POST['password2']
    return redirect(f'/main/profile/{request.user.id}')

def logout_view(request):
    logout(request)
    #messages.add_message(request, messages.SUCCESS, "Logged Out")
    return redirect("/main/", permanent=True)