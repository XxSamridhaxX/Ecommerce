from django.shortcuts import render,redirect
from .models import Product, Order, OrderItem, ShippingAddress, Customer, OrderItem
from django.db.models import F,ExpressionWrapper, FloatField
from django.http import JsonResponse
import json


from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # create unique id for duplicate orders
# Create your views here.


from .utils import cookieCart, cartData, guestOrder

def store(request):

    Data = cartData(request)
    items = Data['items']
    order = Data['order']
    cartItems = Data['cartItems']
    products = Product.objects.all()
    context= {'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)


def cart(request):

    Data = cartData(request)
    items = Data['items']
    order = Data['order']
    cartItems = Data['cartItems']

    context= {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def checkout(request):

    Data = cartData(request)
    items = Data['items']
    order = Data['order']
    cartItems = Data['cartItems']
    context= {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


# Order ma plus or minus or add to cart gareko cha bhane yo view chalcha
def updateItem(request):
    # Aba frontend bata data aucha json ma teslai parse garnu parcha

    data = json.loads(request.body)
    # data ma load huncha parsed Json tya bata product ra action nikalne
    productID = data['productId']
    action = data['action']
    print('Action: ',action)
    print('Product: ',productID)

    customer = request.user.customer
    product = Product.objects.get(id=productID)

    # if tyo cart ma add gareko item Order(cart in general) chaina bhane add it in order model
    order,created = Order.objects.get_or_create(customer=customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product= product)

    if action=="add":
        orderItem.quantity+=1

    elif action=="remove":
        orderItem.quantity-=1
    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    
    return JsonResponse('Item was added', safe = False)

import datetime
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def processOrder(request):
    transation_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)


        

    else:
        """" Fetch bata bhako data request.body ma aucha ani json.loads le python dict ma convert gardincha """
        customer,order = guestOrder(request,data)
            
    order.transaction_id = transation_id
    total = float(data['form']['total'])
    if total == order.get_cart_total:
            order.complete = True
    order.save()

    # Gets its data from request.body which was sent by fetch in this url
    if order.shipping == True:
            ShippingAddress.objects.create(
                 customer = customer,
                order = order,
                address = data["shipping"]['address'],
                city = data['shipping']['city'],
                state = data["shipping"]['state'],
                zipcode = data["shipping"]['zipcode'],
            )
    
    # # PalPal form dictionary
    # paypal_dict = {
         
    # }

    
    return JsonResponse("Payment Submitted..aasdfasdfasdfasdfasd.", safe = False)

