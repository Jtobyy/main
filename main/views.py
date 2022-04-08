from http.client import REQUEST_ENTITY_TOO_LARGE
from multiprocessing import context
import this
from unicodedata import category
from xml.dom.minidom import Document
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User, Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import RegForm, TailorRegForm, SellerRegForm
from .models import CATEGORIES, Clothe, Customer, Fabric, Tailor, Address, Seller, PendingSellerReg, PendingTailorReg
from django.core import serializers
from django.conf import settings
import json
import re
import pickle

from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator

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





# sample views
@login_required(login_url='main/login.html')
def clothe_sample_view(request, clothe_id):
    object = Clothe.objects.get(id=clothe_id)
    return render(request, 'main/clothe.html', {'object': object})

@login_required(login_url='main/login.html')
def fabric_sample_view(request, fabric_id):
    object = Fabric.objects.get(id=fabric_id)
    return render(request, 'main/fabric.html', {'object': object})

def welcome_view(request):
    context = {
        'AnonymousUser': AnonymousUser
    }
    return render(request, 'main/welcome.html', context)




# Shopping
def cart_view(request):    
    referer = request.META.get('HTTP_REFERER')
    print(referer)
    if referer is None or re.match(".+/cart.*", referer) is None:
        print(referer)
        return render(request, 'main/cart.html', None)
    storage = request.GET.get('thestorage')
    if (storage is None):
        return render(request, 'main/cart.html', None)
    basket = json.loads(storage)
    fabrics = basket['fabrics']
    clothes = basket['clothes']
    try:
        cart = []
        total = 0
        for key, val in fabrics.items():
            sep = val.index('_')
            id = val[:sep]
            amount = val[sep+1:]
            fabric_obj = Fabric.objects.get(id=id)
            total += fabric_obj.price * int(amount)
            thisfabric = fabric_obj
            thisfabric.amount = amount
            cart.append(thisfabric)
        for key, val in clothes.items():
            sep = val.index('_')  
            id = val[:sep]
            amount = val[sep+1:]
            clothe_obj = Clothe.objects.get(id=id)
            total += clothe_obj.price * int(amount)
            thisclothe = clothe_obj
            thisclothe.amount = amount
            cart.append(thisclothe)
        context = {
            'cart': cart,
            'total': total
        }
        return render(request, 'main/cart/mycart.html', context)
    except Exception as e:
        #print(e)
        return render(request, 'main/cart/mycart.html', None)

def shop_view(request):
    #print('here first')    
    clothes = Clothe.objects.all()
    paginator = Paginator(clothes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/shop.html', {'page_obj': page_obj})    

def shop_filter_view(request):
    if request.method == 'POST':
        clothes_arrays = []
        categories = request.POST
        if len(request.POST) <= 1:
            return redirect('/main/shop')
        for key in categories:
            clothes = Clothe.objects.filter(category__icontains = key)#.distinct('id')
            if len(clothes) > 0:
                clothes_arrays.append(list(clothes))
        clothes_array = [item for sublist in clothes_arrays for item in sublist]
        pickle_out = open("dict.pickle", "wb")
        pickle.dump(clothes_array, pickle_out)
        pickle_out.close()
        catpickle_out = open("dict.catpickle", "wb")
        pickle.dump(categories, catpickle_out)
        catpickle_out.close()
        paginator = Paginator(clothes_array, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'categories': categories
        }
        return render(request, 'main/shop.html', context)
    else:
        try:    
            pickle_in = open("dict.pickle", "rb")
            catpickle_in = open("dict.catpickle", "rb")
            clothes_array = pickle.load(pickle_in)
            #print(clothes_array)
            categories = pickle.load(catpickle_in)
            paginator = Paginator(clothes_array, 8)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'page_obj': page_obj,
                'categories': categories
            }
            return render(request, 'main/shop.html', context)
        except:
            return redirect('/main/shop')

def ex_shop_filter_view(request, filter):
    #print('got here')
    clothes_arrays = []
    categories = []
    categories.append(filter)
    for key in categories:
        clothes = Clothe.objects.filter(category__icontains = key)#.distinct('id')
        if len(clothes) > 0:
            clothes_arrays.append(list(clothes))
    clothes_array = [item for sublist in clothes_arrays for item in sublist]
    pickle_out = open("dict.pickle", "wb")
    pickle.dump(clothes_array, pickle_out)
    pickle_out.close()
    catpickle_out = open("dict.catpickle", "wb")
    pickle.dump(categories, catpickle_out)
    catpickle_out.close()
    paginator = Paginator(clothes_array, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'categories': categories
    }
    return render(request, 'main/shop.html', context)

def fabrics_view(request):
    fabrics = Fabric.objects.all()
    paginator = Paginator(fabrics, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/fabrics.html', {'fabrics': page_obj})

def fabrics_filter_view(request):
    if request.method == 'POST':
        fabrics_arrays = []
        types = request.POST
        if len(request.POST) <= 1:
            return redirect('/main/fabrics')
        for key in types:
            fabrics = Fabric.objects.filter(type__icontains = key)#.distinct('id')
            if len(fabrics) > 0:
                fabrics_arrays.append(list(fabrics))
        fabrics_array = [item for sublist in fabrics_arrays for item in sublist]
        pickle_out = open("fabdict.pickle", "wb")
        pickle.dump(fabrics_array, pickle_out)
        pickle_out.close()
        typepickle_out = open("fabdict.typepickle", "wb")
        pickle.dump(types, typepickle_out)
        typepickle_out.close()
        paginator = Paginator(fabrics_array, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(page_obj)
        context = {
            'fabrics': page_obj,
            'types': types
        }
        return render(request, 'main/fabrics.html', context)
    else:
        try:    
            pickle_in = open("fabdict.pickle", "rb")
            typepickle_in = open("fabdict.typepickle", "rb")
            fabrics_array = pickle.load(pickle_in)
            #print(fabrics_array)
            types = pickle.load(typepickle_in)
            paginator = Paginator(fabrics_array, 8)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'page_obj': page_obj,
                'types': types
            }
            return render(request, 'main/fabrics.html', context)
        except:
            return redirect('/main/fabrics')

def ex_fabrics_filter_view(request, filter):
    fabrics_arrays = []
    types = []
    types.append(filter)
    for key in types:
        fabrics = Fabric.objects.filter(type__icontains = key)#.distinct('id')
        if len(fabrics) > 0:
            fabrics_arrays.append(list(fabrics))
    fabrics_array = [item for sublist in fabrics_arrays for item in sublist]
    pickle_out = open("fabdict.pickle", "wb")
    pickle.dump(fabrics_array, pickle_out)
    pickle_out.close()
    typepickle_out = open("fabdict.typepickle", "wb")
    pickle.dump(types, typepickle_out)
    typepickle_out.close()
    paginator = Paginator(fabrics_array, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'fabrics': page_obj,
        'types': types
    }
    return render(request, 'main/fabrics.html', context)




# tailor profile section
@login_required(login_url='main/login.html')
def external_profile_view(request, user):
    try:
        thisuser = User.objects.get(username=user)
        tailor = Tailor.objects.get(user=thisuser.id)
        clothes = Clothe.objects.filter(company_name=thisuser.id)
        context = {
            'clothes': clothes,
            'tailor': tailor
        }
        return render(request, 'main/profile2.html', context)
    except Exception as e:
        thisuser = User.objects.get(username=user)
        seller = Tailor.objects.get(user=thisuser.id)
        clothes = Clothe.objects.filter(company_name=thisuser.id)
        context = {
            'clothes': clothes,
            'seller': seller
        }
        return render(request, 'main/profile2.html', context)
    
@login_required(login_url='main/login.html')
def tailor_profile_view(request, tailor_id):
    tailor = Tailor.objects.get(id=tailor_id)
    user = User.objects.get(tailor=tailor)
    try:
        location = Address.objects.get(user=request.user.id)
    except:
        location = None
    userdetails = {
        'username': user.username,
        'email': user.email,
        'phone_no1': tailor.phone_no1,
        'phone_no2': tailor.phone_no2,
        'this_address': location
    } 
    clothes = Clothe.objects.filter(company_name=request.user)
    details = request.GET
    try:
        section = details.get('section')
        if section == 'account':
            view = details.get('view')
            if view == 'overview':
                return render(request, 'main/profile/account.html', {'userdetails': userdetails})
            elif view == 'accountdetails':
                return render(request, 'main/profile/accountdetails.html', {'userdetails': userdetails})
            elif view == 'addressedit':
                address_id = int(details['id'])
                userdetails['this_address'] = Address.objects.get(id=address_id)
                return render(request, 'main/profile/addressdetail.html', {'userdetails': userdetails})
            elif view == 'newaddress':
                return render(request, 'main/profile/addressoutline.html', None)

        if section == 'inbox':
            return render(request, 'main/profile/inbox.html', None)
        if section == 'payment':
            return render(request, 'main/profile/payment.html', None)
        if section == 'orders':
            return render(request, 'main/profile/orders.html', None)
    except Exception as e:
        return render(request, 'main/profile/account.html', None)
    return render(request, 'main/profile.html', {'userdetails': userdetails})

@login_required(login_url='main/login.html')
def edit_tailor_view(request, tailor_id):
    if request.method == 'POST':
        details = request.POST
        thistailor = Tailor.objects.get(id=tailor_id)
        thisuser = User.objects.get(tailor=thistailor)
        
        # update email if present
        if len(details.get('email', '#')) > 1:
            thisuser.email = details.get('email')

        # update rest of tailor's data
        if len(details.get('phone_no1', '#')) > 1:
            thistailor.phone_no1 = details.get('phone_no1')
        if len(details.get('phone_no2', '#')) > 1:
            thistailor.phone_no2 = details.get('phone_no2')
                
        try:
            thistailor.profile_image = request.FILES['profile_image']
        except MultiValueDictKeyError:
            pass

        thisuser.save()
        thistailor.save()
        return redirect(f'/main/tailorProfile/{tailor_id}')
    return render(request, 'main/profile.html', None)    

@login_required(login_url='main/login.html')
def tailors_list_view(request):
    tailors = Tailor.objects.all()
    paginator = Paginator(tailors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/tailors.html', {'page_obj': page_obj})  




# Seller profile section
def seller_profile_view(request, seller_id):    
    seller = Seller.objects.get(id=seller_id)
    user = User.objects.get(seller=seller)
    try:
        location = Address.objects.get(user=request.user.id)
    except:
        location = None
    userdetails = {
        'username': user.username,
        'email': user.email,
        'phone_no1': seller.phone_no1,
        'phone_no2': seller.phone_no2,
        'this_address': location
    } 
    clothes = Clothe.objects.filter(company_name=request.user)
    details = request.GET
    try:    
        section = details.get('section')
        if section == 'account':
            view = details.get('view')
            if view == 'overview':
                return render(request, 'main/profile/account.html', {'userdetails': userdetails})
            elif view == 'accountdetails':
                return render(request, 'main/profile/accountdetails.html', {'userdetails': userdetails})
            elif view == 'addressedit':
                address_id = int(details['id'])
                userdetails['this_address'] = Address.objects.get(id=address_id)
                return render(request, 'main/profile/addressdetail.html', {'userdetails': userdetails})
            elif view == 'newaddress':
                return render(request, 'main/profile/addressoutline.html', None)

        if section == 'inbox':
            return render(request, 'main/profile/inbox.html', None)
        if section == 'payment':
            return render(request, 'main/profile/payment.html', None)
        if section == 'orders':
            return render(request, 'main/profile/orders.html', None)
    except Exception as e:
        return render(request, 'main/profile/account.html', None)
    return render(request, 'main/profile.html', {'userdetails': userdetails})


def edit_seller_view(request, seller_id):
    if request.method == 'POST':
        details = request.POST
        thisseller = Seller.objects.get(id=seller_id)
        thisuser = User.objects.get(seller=thisseller)
        
        # update email if present
        if len(details.get('email', '#')) > 1:
            thisuser.email = details.get('email')

        # update rest of seller's data
        if len(details.get('phone_no1', '#')) > 1:
            thisseller.phone_no1 = details.get('phone_no1')
        if len(details.get('phone_no2', '#')) > 1:
            thisseller.phone_no2 = details.get('phone_no2')
                
        try:
            thisseller.profile_image = request.FILES['profile_image']
        except MultiValueDictKeyError:
            pass

        thisuser.save()
        thisseller.save()
        return redirect(f'/main/sellerProfile/{seller_id}')
    return render(request, 'main/profile.html', None)    




# customer profile section
@login_required(login_url='main/login.html')
def customer_profile_view(request, customer_id):
    print(request.META.get('HTTP_REFERER'))    
    customer = Customer.objects.get(id=customer_id)
    user = User.objects.get(customer=customer)
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
                return render(request, 'main/profile/account.html', {'userdetails': userdetails})
            elif view == 'accountdetails':
                return render(request, 'main/profile/accountdetails.html', {'userdetails': userdetails})
            elif view == 'addressbook':
                addresses = Address.objects.filter(user=request.user)
                userdetails['addresses'] = addresses
                return render(request, 'main/profile/addressbook.html', {'userdetails': userdetails})
            elif view == 'defaultaddress':
                return render(request, 'main/profile/addressdetail.html', {'userdetails': userdetails})
            elif view == 'newaddress':
                return render(request, 'main/profile/addressoutline.html', None)
            elif view == 'addressedit':
                address_id = int(details['id'])
                try:
                    if details.get('action') == 'delete':
                        Address.objects.get(id=address_id).delete()
                        addresses = Address.objects.filter(user=request.user)
                        userdetails['addresses'] = addresses
                        return render(request, 'main/profile/addressbook.html', {'userdetails': userdetails})
                except:
                    pass    
                userdetails['this_address'] = Address.objects.get(id=address_id)
                return render(request, 'main/profile/addressdetail.html', {'userdetails': userdetails})
            elif view == 'inbox':
                return render(request, 'main/profile/inbox.html', {'userdetails': userdetails})
            elif view == 'payment':
                return render(request, 'main/profile/payment.html', {'userdetails': userdetails})

        if section == 'inbox':
            return render(request, 'main/profile/inbox.html', None)
        if section == 'payment':
            return render(request, 'main/profile/payment.html', None)
        if section == 'orders':
            return render(request, 'main/profile/orders.html', None)
        if section == 'measurement':
            view = details.get('view')    
            if view == 'steps':
                return render(request, 'main/profile/measurementsteps.html', None)    
            elif view == 'requestpro':
                return render(request, 'main/profile/requestpro.html', None)    
            return render(request, 'main/profile/measurementdetailsm.html', None)
    except Exception as e:
        return render(request, 'main/profile/account.html', None)
    return render(request, 'main/profile.html', {'userdetails': userdetails})

@login_required(login_url='main/login.html')
def edit_customer_view(request, customer_id):
    if request.method == "POST":
        details = request.POST
        thiscustomer = Customer.objects.get(id=customer_id)
        thisuser = User.objects.get(customer=thiscustomer)
        
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
        return redirect(f'/main/custProfile/{customer_id}')
    return render(request, 'main/profile.html', None)




# Address
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
            newaddress.default = False
        newaddress.save()
    customer_group = Group.objects.get(name='Customers')
    tailor_group = Group.objects.get(name='Tailors')
    seller_group = Group.objects.get(name='Sellers')
    if request.user in customer_group.user_set.all():
        return redirect(f'/main/custProfile/{request.user.customer.id}')
    elif request.user in tailor_group.user_set.all():    
        return redirect(f'/main/tailorProfile/{request.user.tailor.id}')    
    elif request.user in seller_group.user_set.all():
        return redirect(f'/main/sellerProfile/{request.user.seller.id}')    
    return redirect(f'/main/custProfile/{request.user.customer.id}')

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
    customer_group = Group.objects.get(name='Customers')
    tailor_group = Group.objects.get(name='Tailors')
    seller_group = Group.objects.get(name='Sellers')
    if request.user in customer_group.user_set.all():
        return redirect(f'/main/custProfile/{request.user.customer.id}')
    elif request.user in tailor_group.user_set.all():
        return redirect(f'/main/tailorProfile/{request.user.tailor.id}')    
    elif request.user in seller_group.user_set.all():
        return redirect(f'/main/sellerProfile/{request.user.seller.id}')    
    return redirect(f'/main/custProfile/{request.user.customer.id}')

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
    customer_group = Group.objects.get(name='Customers')
    tailor_group = Group.objects.get(name='Tailors')
    seller_group = Group.objects.get(name='Sellers')
    if request.user in customer_group.user_set.all():
        return redirect(f'/main/custProfile/{request.user.customer.id}')
    elif request.user in tailor_group.user_set.all():
        return redirect(f'/main/tailorProfile/{request.user.tailor.id}')
    elif request.user in seller_group.user_set.all():
        return redirect(f'/main/sellerProfile/{request.user.seller.id}')
    return redirect(f'/main/custProfile/{request.user.customer.id}')



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
                return redirect(f"/main/custProfile/{request.user.customer.id}", permanent=True)
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
            return redirect(f"/main/custProfile/{request.user.customer.id}", permanent=True)
        if option == 'opt4':
            return redirect(f"/main/custProfile/{request.user.customer.id}", permanent=True)
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
        return redirect(f'/main/custProfile/{request.user.customer.id}')
    return render(request, 'main/measure/requestpro.html', None)




# Registration
def tailor_reg_info_view(request):
    return render(request, 'main/regtailorinfo.html', None)

def seller_reg_info_view(request):
    return render(request, 'main/regsellerinfo.html', None)

def tailor_reg_view(request):
    if request.method == 'POST':
        form = TailorRegForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/reg/regsuccess.html', None)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    form = TailorRegForm()
    #print('got here with', form.errors)
    return render(request, 'main/reg/regtailor.html', {'form': form})

def seller_reg_view(request):
    if request.method == 'POST':
        form = SellerRegForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/reg/regsuccess.html', None)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    form = SellerRegForm()
    return render(request, 'main/reg/regseller.html', {'form': form})

def register_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
        return redirect("/main/auth")
    else:
        if request.method == "POST":
            form = RegForm(request.POST)
            
            if form.is_valid():    
                user = form.save()    
                if user == False:
                    messages.add_message(request, messages.ERROR, "Email already registered")    
                    return redirect(f'/main/auth?thisform=signup')
                username = user.username
                group = Group.objects.get(name='Customers')
                group.user_set.add(User.objects.get(username = username))
                user = authenticate(request, username=username, 
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





# Authentication
def popauth_view(request):
    return render(request, 'main/popauth.html', {'test': 'test'})

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
            #print(username)
            #print(password)
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
        
@login_required(login_url='main/login.html')
def change_user_pass(request):
    #if request.method == 'POST':
    #   if request.user.is_authenticated():
    user = User.objects.get(id=request.user.id)
    user.password1 = request.POST['password1']
    user.password2 = request.POST['password2']
    #else:
    #        return redirect(f'/main/auth')
    customer_group = Group.objects.get(name='Customers')
    tailor_group = Group.objects.get(name='Tailors')
    seller_group = Group.objects.get(name='Sellers')
    if request.user in customer_group.user_set.all():
        return redirect(f'/main/custProfile/{request.user.customer.id}')
    elif request.user in tailor_group.user_set.all():
        return redirect(f'/main/tailorProfile/{request.user.tailor.id}')    
    elif request.user in seller_group.user_set.all():
        return redirect(f'/main/sellerProfile/{request.user.seller.id}')
    return redirect(f'/main/custProfile/{request.user.customer.id}')
    
    
    #else:
    #    return render(request, 'main/forgotp.html', None)
    

def logout_view(request):
    logout(request)
    #messages.add_message(request, messages.SUCCESS, "Logged Out")
    return redirect("/main/", permanent=True)












# unused
"""
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
"""