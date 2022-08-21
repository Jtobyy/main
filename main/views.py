from datetime import datetime, timedelta
from django.db.models import Q
from notifications.signals import notify
from urllib.request import urlopen, Request
from django.contrib import messages
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import hashers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from .forms import RegForm, FabricForm, CustomClothForm, SewedClothForm
from .models import CATEGORIES, CUSTOMCLOTHES, FABRICS, USERS, Cloth, CustomMadeOrder, FemaleCustomerMeasurement, MaleCustomerMeasurement, SewedClothOrder
from .models import Customer, Fabric, Address, PendingReg, CustomMadeCloth, SewedCloth
from .models import Partner, FabricOrder, FabricSeller, CustomMadeSeller, Tailor, BANK
# from .tokens import account_activation_token
from django.conf import settings
import json
import re
import pickle
import uuid

from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
# from django.utils.encoding import force_bytes, force_text



# sample views
def cloth_sample_view(request, cloth_id):
    object = Cloth.objects.get(id=cloth_id)
    return render(request, 'main/cloth.html', {'object': object})

def fabric_sample_view(request, fabric_id):
    object = Fabric.objects.get(id=fabric_id)
    return render(request, 'main/fabric.html', {'object': object})

def welcome_view(request):
    context = {
        'AnonymousUser': AnonymousUser
    }
    return render(request, 'main/welcome.html', context)

def partner_view(request):
    return render(request, 'main/partner.html', None)




# Shopping
def cart_view(request):
     # Get transaction data
    if request.GET.get('status') == 'successful':
        transaction_id = request.GET.get('transaction_id')
        if transaction_id is None:
            return render(request, 'main/cart.html', None)
        url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
        try:
            req = Request(url)
            req.add_header('Authorization', 'Bearer FLWSECK_TEST-f88bc3ce9942f9dd43bdb389f2c5e24e-X')
            response = urlopen(req)
            content = json.load(response)
            pickle_in_name = str(request.user.id)+"tx_ref.pickle"
            pickle_in = open(pickle_in_name, "rb")
            tx_ref = pickle.load(pickle_in)
            if str(tx_ref) == str(content['data']['tx_ref']):
                cart_name = str(request.user.id)+"cart.pickle"
                cart_total_name = str(request.user.id)+"cart_total.pickle"
                cart = pickle.load(open(cart_name, "rb"))
                cart_total = pickle.load(open(cart_total_name, "rb"))
                
                for obj in cart: # Create an order instance for each Item
                    if obj.item == 'fabric':
                        fabric = Fabric.objects.filter(id = obj.id)[0]
                        if fabric is not None:
                            fabric.order_amount += 1
                            fabric.save()    
                            fabric_order = FabricOrder(order_id=transaction_id, order_item=fabric, order_customer=request.user.customer,
                                                       order_partner=fabric.partner, order_quantity=obj.amount, order_total_price=int(cart_total),
                                                       order_status='P')
                            fabric_order.save()
                            sender = fabric_order.order_customer
                            recipient = fabric_order.order_partner
                            message = f"Order for {fabric_order.order_quantity} yard(s) of your fabric \
                            which is labelled {fabric_order.order_item.label}"
                            notify.send(sender=sender.user, action_object=fabric_order,
                            level='info', recipient=recipient.user, verb='notification', description=message)
                    elif obj.item == 'cloth':
                        cloth = Cloth.objects.filter(id = obj.id)[0]
                        if cloth is not None:
                            cloth.order_amount += 1
                            cloth.save()
                            if cloth.company.brand_type == 'T':
                                cloth_order = SewedClothOrder(order_id=transaction_id, order_item=cloth, order_customer=request.user.customer,
                                                        order_partner=cloth.company, order_quantity=obj.amount, order_total_price=int(cart_total),
                                                        order_status='P')
                            elif cloth.company.brand_type == 'C':
                                cloth_order = CustomMadeOrder(order_id=transaction_id, order_item=cloth, order_customer=request.user.customer,
                                                        order_partner=cloth.company, order_quantity=obj.amount, order_total_price=int(cart_total),
                                                        order_status='P')
                            cloth_order.save()
                            sender = cloth_order.order_customer
                            recipient = cloth_order.order_partner
                            message = f"Order for cloth labelled {cloth_order.order_item.label}"
                            notify.send(sender=sender.user, action_object=cloth_order,
                            level='info', recipient=recipient.user, verb='notification', description=message)
                messages.add_message(request, messages.SUCCESS, "order successful")
                return redirect(f'/main/custProfile/{request.user.customer.id}?exsection=order')
        except Exception as e:
            print(e)
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/cart.*", referer) is None:    
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
            thisfabric.item = 'fabric'
            cart.append(thisfabric)
        for key, val in clothes.items():
            sep = val.index('_')
            id = val[:sep]
            amount = val[sep+1:]
            print(amount)
            cloth_obj = Cloth.objects.filter(id=id)[0]
            total += cloth_obj.price * int(amount)
            thiscloth = cloth_obj
            thiscloth.amount = amount
            thiscloth.item = 'cloth'
            cart.append(thiscloth)
        tx_ref = uuid.uuid4()
        tx_ref_pickle_name = str(request.user.id)+"tx_ref.pickle"
        pickle_out = open(tx_ref_pickle_name, "wb")
        pickle.dump(tx_ref, pickle_out)
        pickle_out.close()

        # Store cart items in a pickle data
        cart_pickle_name = str(request.user.id)+"cart.pickle"
        cart_pickle = open(cart_pickle_name, "wb")
        pickle.dump(cart, cart_pickle)
        cart_pickle.close()

        # Store cart total value in a pickle data
        cart_value_name = str(request.user.id)+"cart_total.pickle"
        cart_total = open(cart_value_name, "wb")
        pickle.dump(total, cart_total)
        cart_total.close()
        
        context = {
            'cart': cart,
            'total': total,
            'tx_ref': tx_ref,
        }
        return render(request, 'main/cart/mycart.html', context)
    except Exception as e:
        return render(request, 'main/cart/mycart.html', None)


def shop_view(request):
    c_orders = list(CustomMadeOrder.objects.filter(order_date__range=[datetime.today()-timedelta(days=20), datetime.today()]))
    s_orders = list(SewedClothOrder.objects.filter(order_date__range=[datetime.today()-timedelta(days=20), datetime.today()]))
    t_orders = c_orders + s_orders
    femaleclothes1 = CustomMadeCloth.objects.filter(Q(category__icontains='JS') or Q(category__icontains='CT')
                                              or Q(category__icontains='JK') or Q(category__icontains='BL')
                                              or Q(category__icontains='GO') or Q(category__icontains='SK')
                                              or Q(category__icontains='NK') or Q(category__icontains='DR'))
    femaleclothes2 = SewedCloth.objects.filter(Q(category__icontains='F'))
    femaleclothes = list(femaleclothes1) + list(femaleclothes2)
    maleclothes1 = CustomMadeCloth.objects.filter(Q(category__icontains='SU') or Q(category__icontains='CS')
                                              or Q(category__icontains='JK') or Q(category__icontains='MT')
                                              or Q(category__icontains='MS') or Q(category__icontains='SH')
                                              or Q(category__icontains='CP') or Q(category__icontains='CO'))
    maleclothes2 = SewedCloth.objects.filter(Q(category__icontains='M'))
    maleclothes = list(maleclothes1) + list(maleclothes2)
    tribe1 = CustomMadeCloth.objects.filter(Q(category__icontains='NW'))
    tribe2 = SewedCloth.objects.filter(Q(category__icontains='T'))
    tribes = list(tribe1) + list(tribe2)
    clothes1 = CustomMadeCloth.objects.all()
    clothes2 = SewedCloth.objects.all()
    clothes = list(clothes1) + list(clothes2)
    paginator = Paginator(clothes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        't_orders': t_orders[:10],
        'femaleclothes': femaleclothes,
        'maleclothes': maleclothes,
        'tribes': tribes,
    }
    return render(request, 'main/shop.html', context)

def shop_filter_view(request):
    if request.method == 'POST':
        clothes_arrays = []
        categories = request.POST
        if len(request.POST) <= 1:
            return redirect('/main/shop')
        for key in categories:
            clothes = Cloth.objects.filter(category__icontains = key)#.distinct('id')
            if len(clothes) > 0:
                clothes_arrays.append(list(clothes))
        clothes_array = [item for sublist in clothes_arrays for item in sublist]
        pickle_out = open("dict.pickle", "wb")
        pickle.dump(clothes_array, pickle_out)
        pickle_out.close()
        catpickle_out = open("dict.catpickle", "wb")
        pickle.dump(categories, catpickle_out)
        catpickle_out.close()
        paginator = Paginator(clothes_array, 9)
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
            categories = pickle.load(catpickle_in)
            paginator = Paginator(clothes_array, 9)
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
    clothes_arrays = []
    categories = []
    categories.append(filter)
    for key in categories:
        clothes1 = CustomMadeCloth.objects.filter(category__icontains = key)#.distinct('id')
        clothes2 = SewedCloth.objects.filter(category__icontains = key)#.distinct('id')
        if len(clothes1) > 0:
            clothes_arrays.append(list(clothes1))
        if len(clothes2) > 0:
            clothes_arrays.append(list(clothes2))
    clothes_array = [item for sublist in clothes_arrays for item in sublist]
    pickle_out = open("dict.pickle", "wb")
    pickle.dump(clothes_array, pickle_out)
    pickle_out.close()
    catpickle_out = open("dict.catpickle", "wb")
    pickle.dump(categories, catpickle_out)
    catpickle_out.close()
    paginator = Paginator(clothes_array, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'categories': categories
    }
    return render(request, 'main/shop.html', context)

def fabrics_view(request):
    fabrics = Fabric.objects.all()
    paginator = Paginator(fabrics, 9)
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
        paginator = Paginator(fabrics_array, 9)
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
            paginator = Paginator(fabrics_array, 9)
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
    paginator = Paginator(fabrics_array, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'fabrics': page_obj,
        'types': types
    }
    return render(request, 'main/fabrics.html', context)

def add_fabric_view(request):
    if request.method == 'POST':
        new_fabric = Fabric()    
        fabric_details = request.POST
        fabric_image = request.FILES
        new_fabric.label = fabric_details.get('label')
        new_fabric.partner = request.user.partner
        new_fabric.type = fabric_details.get('type')
        new_fabric.per_yard = fabric_details.get('per_yard')
        new_fabric.price = fabric_details.get('price')
        new_fabric.image = fabric_image['image']
        new_fabric.save()
        messages.add_message(request, messages.SUCCESS, "Fabric successfully added")
        return redirect(f'partnerProfile/{request.user.partner.id}')

def add_cloth_view(request):
    if request.method == 'POST':
        new_cloth = Cloth()
        cloth_details = request.POST
        cloth_image = request.FILES
        new_cloth.label = cloth_details.get('label')
        new_cloth.company = request.user.partner
        new_cloth.price = cloth_details.get('price')
        new_cloth.image = cloth_image['image']
        new_cloth.save()

        cloth_link = CustomMadeCloth() if request.user.partner.brand_type == 'C' else SewedCloth()
        cloth_link.cloth_object = new_cloth
        cloth_link.category = dict(cloth_details)['type']
        cloth_link.save()

        messages.add_message(request, messages.SUCCESS, "Sample successfully added")
        return redirect(f'partnerProfile/{request.user.partner.id}')




# Partners profile section
def partner_profile_view(request, partner_id):
    partner = Partner.objects.get(id=partner_id)
    user = User.objects.get(partner=partner)
    userdetails = partner.__dict__
    userdetails.update(user.__dict__)
    context = {
        'userdetails': userdetails
    }
    details = request.GET
    try:
        section = details.get('section')
        if section == 'account':
            return render(request, 'main/profile3/account.html', context)
        elif section == 'contactinfo':
            return render(request, 'main/profile3/editcontactinfo.html', context)
        elif section == 'payment':
            partner = Partner.objects.get(id=request.user.partner.id)
            bank = None   
            for val in BANK:
                if val[0] == partner.bank:
                    bank = val[1]
                    break
            return render(request, 'main/profile3/payment.html', {'bank': bank})
        elif section == 'specialization':
            try:    
                if request.user.partner.brand_type == 'F':
                    values = FABRICS    
                    seller = FabricSeller.objects.get(partner=request.user.partner) 
                elif request.user.partner.brand_type == 'C':
                    values = CUSTOMCLOTHES    
                    seller = CustomMadeSeller.objects.get(partner=request.user.partner) 
                elif request.user.partner.brand_type == 'T':
                    values = CATEGORIES    
                    seller = Tailor.objects.get(partner=request.user.partner)
            except:
                if request.user.partner.brand_type == 'F':
                    values = FABRICS    
                elif request.user.partner.brand_type == 'C':
                    values = CUSTOMCLOTHES    
                elif request.user.partner.brand_type == 'T':
                    values = CATEGORIES    
                seller = None
            context = {
                'form_values': values,
                'seller': seller,
            }
            return render(request, 'main/profile3/specialization.html', context)
        elif section == 'security':
            return render(request, 'main/profile3/security.html', context)
        elif section == 'notifications':
            user = User.objects.get(id=request.user.id)    
            notifications = user.notifications.read()
            return render(request, 'main/notifications.html', {'read_notifications': notifications})
        elif section == 'editpassword':
            return render(request, 'main/profile3/password.html', context)
        elif section == 'market':
            if request.user.partner.brand_type == 'F':
                objects = Fabric.objects.filter(partner=request.user.partner).count()
                not_accepted = FabricOrder.objects.filter(order_partner = request.user.partner,
                                                          order_status='P').count()
                accepted = FabricOrder.objects.filter(order_partner = request.user.partner,
                                                      order_status='C').count()
                ready = FabricOrder.objects.filter(order_partner = request.user.partner,
                                                   order_status='R').count()
                sold = FabricOrder.objects.filter(order_partner = request.user.partner,
                                                       order_status='D').count()
            elif request.user.partner.brand_type == 'C':
                objects = Cloth.objects.filter(company=request.user.partner).count()
                not_accepted = CustomMadeOrder.objects.filter(order_partner = request.user.partner,
                                                          order_status='P').count()
                accepted = CustomMadeOrder.objects.filter(order_partner = request.user.partner,
                                                      order_status='C').count()
                ready = CustomMadeOrder.objects.filter(order_partner = request.user.partner,
                                                   order_status='R').count()
                sold = CustomMadeOrder.objects.filter(order_partner = request.user.partner,
                                                       order_status='D').count()
            elif request.user.partner.brand_type == 'T':
                objects = Cloth.objects.filter(company=request.user.partner).count()
                not_accepted = SewedClothOrder.objects.filter(order_partner = request.user.partner,
                                                          order_status='P').count()
                accepted = SewedClothOrder.objects.filter(order_partner = request.user.partner,
                                                      order_status='C').count()
                ready = SewedClothOrder.objects.filter(order_partner = request.user.partner,
                                                   order_status='R').count()
                sold = SewedClothOrder.objects.filter(order_partner = request.user.partner,
                                                       order_status='D').count()
                
            context = {
                'market': objects,
                'not_accepted_no': not_accepted,
                'accepted_no': accepted,
                'ready_no': ready,
                'delivered_no': sold,
            }
            return render(request, 'main/profile3/market.html', context)

        elif section == 'pendingorders':
            if request.user.partner.brand_type == 'F':    
                pending_orders = FabricOrder.objects.filter(order_partner=request.user.partner,
                                                        order_status='P')
            elif request.user.partner.brand_type == 'C':
                pending_orders = CustomMadeOrder.objects.filter(order_partner=request.user.partner,
                                                        order_status='P')
            elif request.user.partner.brand_type == 'T':
                pending_orders = SewedClothOrder.objects.filter(order_partner=request.user.partner,
                                                        order_status='P')

            return render(request, 'main/profile3/pendingorders.html', {'pending': pending_orders})
        
        elif section == 'acceptedorders': 
            if request.user.partner.brand_type == 'F':        
                accepted_orders = FabricOrder.objects.filter(order_partner = request.user.partner,
                                                             order_status='C')
            elif request.user.partner.brand_type == 'C':
                accepted_orders = CustomMadeOrder.objects.filter(order_partner = request.user.partner,
                                                                 order_status='C')
            elif request.user.partner.brand_type == 'T':
                accepted_orders = SewedClothOrder.objects.filter(order_partner = request.user.partner,
                                                                 order_status='C')

            return render(request, 'main/profile3/acceptedorders.html', {'accepted': accepted_orders})

        elif section == 'readiedorders':
            if request.user.partner.brand_type == 'F':        
                readied_orders = FabricOrder.objects.filter(order_partner = request.user.partner,
                                                       order_status='R')
            elif request.user.partner.brand_type == 'C':
                readied_orders = CustomMadeOrder.objects.filter(order_partner = request.user.partner,
                                                                 order_status='R')
            elif request.user.partner.brand_type == 'T':
                readied_orders = SewedClothOrder.objects.filter(order_partner = request.user.partner,
                                                                 order_status='R')

            return render(request, 'main/profile3/ready.html', {'readied': readied_orders})

        elif section == 'deliveredorders':
            if request.user.partner.brand_type == 'F':        
                delivered_orders = FabricOrder.objects.filter(order_partner = request.user.partner,
                                                              order_status='D')
            elif request.user.partner.brand_type == 'C':
                delivered_orders = CustomMadeOrder.objects.filter(order_partner = request.user.partner,
                                                                  order_status='D')
            elif request.user.partner.brand_type == 'T':
                delivered_orders = SewedClothOrder.objects.filter(order_partner = request.user.partner,
                                                                  order_status='D')

            return render(request, 'main/profile3/deliveredfabrics.html', {'delivered': delivered_orders})

        elif section == 'fabricorderdetails':
            id = request.GET.get('orderid')
            notificationid = request.GET.get('notificationid')
            if notificationid is not None and notificationid != 'undefined':
                notification = request.user.notifications.filter(id=notificationid)[0]
                notification.mark_as_read()
            order = FabricOrder.objects.filter(id=id)
            context = {
                'order': order[0]
            }
            return render(request, 'main/profile/orderdetails.html', context)
        elif section == 'cclothorderdetails':
            id = request.GET.get('orderid')
            notificationid = request.GET.get('notificationid')
            if notificationid is not None and notificationid != 'undefined':
                notification = request.user.notifications.filter(id=notificationid)[0]
                notification.mark_as_read()
            order = CustomMadeOrder.objects.filter(id=id)
            context = {
                'order': order[0]
            }
            return render(request, 'main/profile/orderdetails.html', context)
        elif section == 'sclothorderdetails':
            id = request.GET.get('orderid')
            notificationid = request.GET.get('notificationid')
            if notificationid is not None and notificationid != 'undefined':
                notification = request.user.notifications.filter(id=notificationid)[0]
                notification.mark_as_read()
            order = SewedClothOrder.objects.filter(id=id)
            context = {
                'order': order[0]
            }
            return render(request, 'main/profile/orderdetails.html', context)
                    
        elif section == 'acceptfabricorder':
            id = request.GET.get('orderid')
            order = FabricOrder.objects.filter(id=id)[0]
            order.order_status = 'C'
            order.save()
            '''notify.send(sender=request.user, action_object=order,
                        level='info', recipient=order.order_customer.user, verb='notification', 
                        description=f"Order for {order.order_quantity} yard(s) of \
                        fabric {order.order_item.label} confirmed. ")'''
            return HttpResponse('accepted')
        elif section == 'acceptcclothorder':
            id = request.GET.get('orderid')
            order = CustomMadeOrder.objects.filter(id=id)[0]
            order.order_status = 'C'
            order.save()
            '''notify.send(sender=request.user, action_object=order,
                        level='info', recipient=order.order_customer.user, verb='notification', 
                        description=f"Order for {order.order_quantity} yard(s) of \
                        fabric {order.order_item.label} confirmed. ")'''
            return HttpResponse('accepted')

        elif section == 'acceptsclothorder':
            id = request.GET.get('orderid')
            order = SewedClothOrder.objects.filter(id=id)[0]
            order.order_status = 'C'
            order.save()
            '''notify.send(sender=request.user, action_object=order,
                        level='info', recipient=order.order_customer.user, verb='notification', 
                        description=f"Order for {order.order_quantity} yard(s) of \
                        fabric {order.order_item.label} confirmed. ")'''
            return HttpResponse('accepted')

        elif section == 'readyfabricorder':
            id = request.GET.get('orderid')
            order = FabricOrder.objects.filter(id=id)[0]
            order.order_status = 'R'
            order.save()
            messages.add_message(request, messages.SUCCESS, "Order ready to be delivered")
            return HttpResponse('readied')
        elif section == 'readycclothorder':
            id = request.GET.get('orderid')
            order = CustomMadeOrder.objects.filter(id=id)[0]
            order.order_status = 'R'
            order.save()
            messages.add_message(request, messages.SUCCESS, "Order ready to be delivered")
            return HttpResponse('readied')
        elif section == 'readysclothorder':
            id = request.GET.get('orderid')
            order = SewedClothOrder.objects.filter(id=id)[0]
            order.order_status = 'R'
            order.save()
            messages.add_message(request, messages.SUCCESS, "Order ready to be delivered")
            return HttpResponse('readied')

        elif section == 'marketobjects':
            if request.user.partner.brand_type == 'F':        
                objects = Fabric.objects.filter(partner=request.user.partner)
            else:
                objects = Cloth.objects.filter(company=request.user.partner)
    
            return render(request, 'main/profile3/allmarkets.html', {'marketobjects': objects})

        elif section == 'addfabric':
            return render(request, 'main/profile3/addfabric.html', {'form': FabricForm()})
        elif section == 'addclothsample':
            form = SewedClothForm() if request.user.partner.brand_type == 'T' else CustomClothForm()
            return render(request, 'main/profile3/addcloth.html', {'form': form})
            
    except Exception as e:
        print(e)
    return render(request, 'main/profile3.html', {'userdetail': userdetails})

@login_required(login_url='main/logoin.html')
def edit_partner_view(request, partner_id):
    if request.method == 'POST':
        details = request.POST    
        partner = Partner.objects.get(id=partner_id)
        thisuser = User.objects.get(partner=partner)
        thisuser.first_name = details['legal_rep_first_name']
        thisuser.last_name = details['legal_rep_last_name']
        partner.legal_rep_first_name = details['legal_rep_first_name']
        partner.legal_rep_other_name = details['legal_rep_other_name']
        partner.legal_rep_last_name = details['legal_rep_last_name']
        partner.address = details['address']
        partner.city = details['city']
        partner.state = details['state']
        partner.zipcode = details['zipcode']
        
        thisuser.save()
        partner.save()
        messages.add_message(request, messages.SUCCESS, 'Updated Successfully')
        return redirect(f'partnerProfile/{partner_id}')

def external_profile_view(request, partner_id):
    partner = Partner.objects.get(id=partner_id)
    if partner.brand_type != 'F':
        market = partner.cloth_set.all()
    context = {
        'market': market,
        'partner': partner,
    }
    return render(request, 'main/profile2.html', context)

def tailors_list_view(request):
    tailors = Tailor.objects.all()
    paginator = Paginator(tailors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/tailors.html', {'page_obj': page_obj})  

@login_required(login_url='main/login.html')
def update_specs_view(request):
    if request.method == 'POST':
        specs = dict(request.POST)['specs']    
        if request.user.partner.brand_type == 'C':
            try:
                partner = CustomMadeSeller.objects.get(partner = request.user.partner)
                partner.specs = specs
                partner.save()
            except:
                partner = CustomMadeSeller(partner=request.user.partner, specs = specs)
                partner.save()
        elif request.user.partner.brand_type == 'T':
            try:
                partner = Tailor.objects.get(partner = request.user.partner)
                partner.specs = specs
                partner.save()
            except:
                partner = Tailor(partner=request.user.partner, specs = specs)
                partner.save()
        elif request.user.partner.brand_type == 'F':
            try:
                seller = FabricSeller.objects.get(partner = request.user.partner)
                seller.specs = specs
                seller.save()
            except:
                seller = FabricSeller(partner=request.user.partner, specs = specs)
                seller.save()
    return redirect(f'partnerProfile/{request.user.partner.id}?exsection=specialization')





# customer profile section
@login_required(login_url='main/login.html')
def customer_profile_view(request, customer_id):
    # print(request.META.get('HTTP_REFERER'))
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
            fabric_orders = FabricOrder.objects.filter(order_customer = request.user.customer)
            custom_cloth_orders = CustomMadeOrder.objects.filter(order_customer = request.user.customer)
            sewed_cloth_orders = SewedClothOrder.objects.filter(order_customer = request.user.customer)
            context = {
                'fabric_orders': fabric_orders,
                'custom_cloth_orders': custom_cloth_orders,
                'sewed_cloth_orders': sewed_cloth_orders,
            }
            return render(request, 'main/profile/orders.html', context)
        if section == 'fabricorderdetails':
            id = request.GET.get('orderid')
            order = FabricOrder.objects.filter(id=id)
            context = {
                'order': order[0]
            }
            return render(request, 'main/profile/orderdetails.html', context)
        elif section == 'cclothorderdetails':
            id = request.GET.get('orderid')
            notificationid = request.GET.get('notificationid')
            if notificationid is not None and notificationid != 'undefined':
                notification = request.user.notifications.filter(id=notificationid)[0]
                notification.mark_as_read()
            order = CustomMadeOrder.objects.filter(id=id)
            context = {
                'order': order[0]
            }
            return render(request, 'main/profile/orderdetails.html', context)

        elif section == 'sclothorderdetails':
            id = request.GET.get('orderid')
            notificationid = request.GET.get('notificationid')
            if notificationid is not None and notificationid != 'undefined':
                notification = request.user.notifications.filter(id=notificationid)[0]
                notification.mark_as_read()
            order = SewedClothOrder.objects.filter(id=id)
            context = {
                'order': order[0]
            }
            return render(request, 'main/profile/orderdetails.html', context)            
            
        if section == 'measurement':
            view = details.get('view')    
            if view == 'steps':
                return render(request, 'main/profile/measurementsteps.html', None)    
            elif view == 'requestpro':
                addresses = Address.objects.filter(user=request.user)
                return render(request, 'main/profile/requestpro.html', {'addresses': addresses})
            if request.user.customer.gender == 'M':
                return render(request, 'main/profile/measurementdetailsm.html', 
                              {'measurement': MaleCustomerMeasurement.objects.get(customer=request.user.customer)})
            else:
                return render(request, 'main/profile/measurementdetailsf.html',
                              {'measurement': FemaleCustomerMeasurement.objects.get(customer=request.user.customer)})

    except Exception as e:
        return render(request, 'main/profile/account.html', None)
    return render(request, 'main/profile.html', {'userdetails': userdetails})

@login_required(login_url='main/login.html')
def customer_profile_image_view(request):
    request.user.customer.profile_image = request.FILES['profile-image']
    request.user.customer.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='main/login.html')
def search_view(request, query):
    fabrics = Fabric.objects.filter(Q(label__icontains = query) | Q(type__icontains = query) |
                                    Q(price__icontains = query) | Q(partner__brand_name__icontains = query))
    clothesR = Cloth.objects.filter(Q(label__icontains = query)  | Q(price__icontains = query) | 
                                    Q(company__brand_name__icontains = query))
    print(query)
    clothes1 = CustomMadeCloth.objects.filter(Q(category__icontains = query))
    clothes2 = SewedCloth.objects.filter(Q(category__icontains = query))
    clothes = list(clothes1) + list(clothes2)
    context = {
        'fabrics': fabrics,
        'clothes': clothes,
        'clothesR': clothesR,
    }
    return render(request, 'main/search_result.html', context)
    

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
        thisuser.first_name = details.get('first_name')
        thisuser.last_name = details.get('last_name')
                
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
    gender = Customer.objects.get(user=request.user).gender
    if gender == 'M':
        return render(request, 'main/measure/measurementdetailsm.html', 
        {'measurement': MaleCustomerMeasurement.objects.get(customer=request.user.customer)})
    elif gender == 'F':
        return render(request, 'main/measure/measurementdetailsf.html',
        {'measurement': FemaleCustomerMeasurement.objects.get(customer=request.user.customer)})

@login_required(login_url='main/auth')
def update_measurement_view(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        gender = customer.gender
        details = dict(request.POST)
        for key, value in details.items():
            try:
                details[key] = float(value[0])   
            except:
                details[key] = 0.00
            
        if gender == 'M':
            male_cust = MaleCustomerMeasurement.objects.get(customer=customer)
            male_cust.round_neck = details.get('round-neck')
            male_cust.shoulder_length = details.get('shoulder-length')
            male_cust.back_shoulder_width = details.get('back-shoulder-width')
            male_cust.front_shoulder_width = details.get('front-shoulder-width')
            male_cust.back_width = details.get('back-width')
            male_cust.round_waist = details.get('round-waist')
            male_cust.waist_length = details.get('waist-length')
            male_cust.back_waist_length = details.get('back-waist-length')
            male_cust.tunic_or_shirt_length = details.get('tunic/shirt-length')
            male_cust.chest_depth = details.get('chest-depth')
            male_cust.chest_width = details.get('chest-width')
            male_cust.round_chest = details.get('round-chest')
            male_cust.round_waist = details.get('round-waist')
            male_cust.round_seat_or_hips = details.get('round-seat/hips')
            male_cust.round_thigh = details.get('round-thigh')
            male_cust.round_knee = details.get('round-knee')
            male_cust.round_ankle = details.get('round-ankle')
            male_cust.waist_to_knee = details.get('waist-to-knee')
            male_cust.waist_to_ankle = details.get('waist-to-ankle')
            male_cust.outside_leg_length = details.get('outside-leg-length')
            male_cust.inside_leg_length = details.get('inside-leg-length')
            male_cust.shoulder_to_elbow = details.get('shoulder-to-elbow')
            male_cust.shoulder_to_wrist = details.get('shoulder-to-wrist')
            male_cust.round_bicep = details.get('round-bicep')
            male_cust.round_arm = details.get('round-arm')
            male_cust.round_wrist = details.get('round-wrist')
            male_cust.save()            

        elif gender == 'F':
            female_cust = FemaleCustomerMeasurement.objects.get(customer=customer)
            female_cust.round_neck =  details.get('round-neck')
            female_cust.shoulder_length =  details.get('shoulder-length')
            female_cust.back_shoulder_width =  details.get('back-shoulder-width')
            female_cust.front_shoulder_width =  details.get('front-shoulder-width')
            female_cust.back_width =  details.get('back-width')
            female_cust.round_waist =  details.get('round-waist')
            female_cust.front_waist_length =  details.get('front-waist-length')
            female_cust.back_waist_length =  details.get('back-waist-length')
            female_cust.blouse_or_shirt_length =  details.get('blouse/shirt-length')
            female_cust.bust_length =  details.get('bust-length')
            female_cust.under_bust_length =  details.get('under-bust-length')
            female_cust.bust_point_separation =  details.get('bust-point-separation')
            female_cust.under_bust_separation =  details.get('under-bust-separation')
            female_cust.high_bust =  details.get('high-bust')
            female_cust.round_bust =  details.get('round-bust')
            female_cust.round_under_bust =  details.get('round-under-bust')
            female_cust.round_abdomen =  details.get('round-abdomen')
            female_cust.round_seat_or_hips =  details.get('round-seat/hips')
            female_cust.round_thigh =  details.get('round-thigh')
            female_cust.round_knee =  details.get('round-knee')
            female_cust.round_ankle =  details.get('round-ankle')
            female_cust.waist_to_hips =  details.get('waist-to-hips')
            female_cust.waist_to_knee =  details.get('waist-to-knee')
            female_cust.waist_to_ankle =  details.get('waist-to-ankle')
            female_cust.outside_leg_length =  details.get('outside-leg-length')
            female_cust.inside_leg_length =  details.get('inside-leg-length')
            female_cust.shoulder_to_elbow =  details.get('shoulder-to-elbow')
            female_cust.shoulder_to_wrist =  details.get('shoulder-to-wrist')
            female_cust.round_bicep =  details.get('round-bicep')
            female_cust.round_arm =  details.get('round-arm')
            female_cust.round_wrist =  details.get('round-wrist')
            female_cust.save()
        return redirect(f"/main/custProfile/{request.user.customer.id}", permanent=True)

@login_required(login_url='main/login.html')
def measurehowto_view(request):
    referer = request.META.get('HTTP_REFERER')
    if referer is None or re.match(".+/auth.*", referer) is None:
        return redirect("/main/auth")
    if request.method == "POST":
        option = request.POST['measureopt']
        if option is None or option == "":
            messages.add_message(request, messages.ERROR, "Please select an option")    
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
                user = authenticate(request, username=username, 
                                    password=request.POST['password1'])
                # Create a customer profile for user after login
                if user is not None:    
                    if request.POST.get('gender'):
                        newcustomer = Customer(user=user, gender=request.POST.get('gender'))
                    else:
                        newcustomer = Customer(user=user)
                    newcustomer.save()
                    if request.POST.get('gender') == 'M':
                        measurement = MaleCustomerMeasurement(customer=newcustomer)
                    elif request.POST.get('gender') == 'F':
                        measurement = FemaleCustomerMeasurement(customer=newcustomer)
                    measurement.save()
                    login(request, user)
                    return redirect("/main/auth?thisform=measureopt")
            messages.add_message(request, messages.ERROR, f"{form.errors}")
            return redirect(f'/main/auth?thisform=signup')
        form = RegForm()
        return render(request, 'main/register.html', {'register_form': form})





# Authentication
def popauth_view(request):
    return render(request, 'main/popauth.html', {'test': 'test'})

def poplogin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:        
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Log in successful")    
            if (user.customer):
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect("/main/")
        else:
            messages.add_message(request, messages.ERROR, "Invalid username or password")
            return redirect(request.META['HTTP_REFERER'])

def popregister_view(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()    
            if user == False:
                messages.add_message(request, messages.ERROR, "Email already registered")    
                return redirect(f'/main/auth?thisform=signup')
            username = user.username
            user = authenticate(request, username=username, 
                                password=request.POST['password1'])
            # Create a customer profile for user after login
            if user is not None:    
                if request.POST.get('gender'):
                    newcustomer = Customer(user=user, gender=request.POST.get('gender'))
                    newcustomer.save()
                else:
                    newcustomer = Customer(user=user)
                    newcustomer.save()
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Log in successful")
                    return redirect("/main/")

                if request.POST.get('gender') == 'M':
                    measurement = MaleCustomerMeasurement(customer=newcustomer)
                    measurement.save()
                elif request.POST.get('gender') == 'F':
                    measurement = FemaleCustomerMeasurement(customer=newcustomer)
                    measurement.save()
                login(request, user)
                return redirect("/main/auth?thisform=measureopt")
        else:
            messages.add_message(request, messages.ERROR, f"{form.errors}")
            return redirect(f'/main/auth?thisform=signup')



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
            email = request.POST['email']
            password = request.POST['password']
            try:
                if request.POST['next']:
                    next = request.POST['next']
            except UnboundLocalError:
                pass
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)    
                if (user.customer):
                    try:
                        return redirect('/main/',next)
                    except UnboundLocalError:
                        return redirect('/main/')
                else:
                    return redirect(f'partnerProfile/{request.user.partner.id}')
            else:
                messages.add_message(request, messages.ERROR, "Invalid email or password")    
                return redirect('/main/auth')
        return render(request, 'main/login.html', None)

def partner_reg_view(request):
    if request.method == 'POST':
        new_reg = PendingReg()
        new_reg.business_entity = request.POST['business_entity']
        new_reg.business_name = request.POST['business_name']
        new_reg.email = request.POST['email']
        new_reg.address = request.POST['address']
        new_reg.city = request.POST['city']
        new_reg.state = request.POST['state']
        new_reg.zipcode = request.POST['zipcode']

        new_reg.brand_name = request.POST['brand_name']
        new_reg.legal_rep_first_name = request.POST['first_name']        
        new_reg.legal_rep_other_name = request.POST['other_name']        
        new_reg.legal_rep_last_name = request.POST['last_name']   
        new_reg.profile_image = request.FILES['profile_image']
        new_reg.valid_id_card = request.FILES['valid_id']
        new_reg.tin = request.POST['tin'] 
        new_reg.vat = request.POST['vat']

        new_reg.brand_type = request.POST['brand_type']

        new_reg.bank = request.POST['bank']   
        new_reg.account_name = request.POST['account_name']
        new_reg.account_number = request.POST['account_number']
        subject = 'Account creation with L\'ayo'
        message = 'Your business profile is under review. Thank you.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['jtobi8161@gmail.com',]
        try:
            send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list, fail_silently=False)
        except:
            pass
        new_reg.save()

        return redirect('/main/request_submitted')
    return render(request, 'main/partner_reg.html', None)

def add_partner_view(request, partner_id):
    # Create a new partner after review    
    pending_partner = PendingReg.objects.get(id = partner_id)
    partner = Partner()
    partner.business_entity = pending_partner.business_entity
    partner.business_name = pending_partner.business_name
    partner.email = pending_partner.email
    partner.address = pending_partner.address
    partner.city = pending_partner.city
    partner.state = pending_partner.state
    partner.zipcode = pending_partner.zipcode

    partner.brand_name = pending_partner.brand_name
    partner.legal_rep_first_name = pending_partner.legal_rep_first_name
    partner.legal_rep_other_name = pending_partner.legal_rep_other_name
    partner.legal_rep_last_name = pending_partner.legal_rep_last_name
    partner.profile_image = pending_partner.profile_image
    partner.valid_id_card = pending_partner.valid_id_card
    partner.tin = pending_partner.tin
    partner.vat = pending_partner.vat

    partner.brand_type = pending_partner.brand_type

    partner.bank = pending_partner.bank
    partner.account_name = pending_partner.account_name
    partner.account_number = pending_partner.account_number

    try:
        # Create random password for the partner    
        password = partner.legal_rep_last_name.lower()+'admin2022'

        new_user = User.objects.create_user(username=partner.email,
                        password=password,
                        first_name=partner.legal_rep_first_name,
                        last_name=partner.legal_rep_last_name,
                        email=partner.email)
        new_user.save()
        partner.user = new_user
        partner.save()
        # Add partner to specific tables depending on their brand type
        if partner.brand_type == 'T':
            new_tailor = Tailor(partner=partner, specs='M')
            new_tailor.save()
        elif partner.brand_type == 'C':
            new_custom_made_seller = CustomMadeSeller(partner=partner)
            new_custom_made_seller.save()
        elif partner.brand_type == 'F':
            new_fabric_seller = FabricSeller(partner=partner)
            new_fabric_seller.save()
        pending_partner.delete()
        # Send an email if account creation was successful
        subject = 'Account Created Successfully Thank you for registering with us.\
            Your registration at layongr has been approved, you can login now and start your journey'

        message = f'Your username is your email address and defult password is {password}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [partner.email]
        send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list, fail_silently=False)
        messages.add_message(request, messages.SUCCESS, 'Profile already created, you can\
                    delete the pending request object to avoid further confusion')
        return redirect('/admin/main/partner')
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, 'Email or Username already in use')
        return redirect(request.META['HTTP_REFERER'])


'''
render_to_string('acc_active_email.html', {
                'user': partner,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(partner.id)).decode(),
                'token':account_activation_token.make_token(partner),
            }),
            
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
        '''

def success_reg_view(request):
    return render(request, 'main/regsubmit.html', None)

@login_required(login_url='main/login.html')
def change_user_pass(request):
    user = User.objects.get(id=request.user.id)
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    user = User.objects.get(id=request.user.id)
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    if (hashers.check_password(old_password, user.password)):
        if new_password == confirm_password:
            user.password = hashers.make_password(new_password)
            user.save()    
            messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
            logout(request)    
            return redirect('/main/auth')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid password')
    else:
        messages.add_message(request, messages.ERROR, 'Old password incorrect')
    if request.user.cutomer:
        return redirect(f'/main/custProfile/{request.user.customer.id}')
    else:
        return redirect(f'/main/partnerProfile/{request.user.partner.id}')
    
@login_required(login_url='main/login.html')
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