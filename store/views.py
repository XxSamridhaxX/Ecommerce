from django.shortcuts import render,redirect
from .models import Product, Order, OrderItem, ShippingAddress, Customer
from django.db.models import F,ExpressionWrapper, FloatField

from django.http import JsonResponse
import json
# Create your views here.


from .utils import cookieCart, cartData

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


def checkout(request):

    Data = cartData(request)
    items = Data['items']
    order = Data['order']
    cartItems = Data['cartItems']

    context= {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


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
def processOrder(request):
    transation_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        order.transaction_id = transation_id
        total = float(data['form']['total'])

        if total == order.get_cart_total:
            order.complete = True
        
        order.save()

        if order.shipping == True:

            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data["shipping"]['address'],
                state = data["shipping"]['state'],
                zipcode = data["shipping"]['zipcode'],
            )

    else:
        anoyData = json.loads(request.body)
        name = anoyData['form']['name']
        email = anoyData['form']['email']

        customer,created = Customer.objects.get_or_create(email = email)
        customer.name= name 
        customer.save()

        order, created = Order.objects.get_or_create(customer = customer)

        # Import data from cookies
        Data = cartData(request)
        items = Data['items']
        order = Data['order']
        cartItems = Data['cartItems']

        for item in items:
            print(item['product']['id'])
            product = Product.objects.get(id = item['product'['id']])

    
    return JsonResponse("Payment Submitted..aasdfasdfasdfasdfasd.", safe = False)

