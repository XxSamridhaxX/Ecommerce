from django.shortcuts import render,redirect
from .models import Product, Order, OrderItem
from django.db.models import F,ExpressionWrapper, FloatField

from django.http import JsonResponse
import json
# Create your views here.

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context= {'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        # items = items.annotate(total = ExpressionWrapper(F('quantity')*F('product__price'),output_field=FloatField()))
        # Expression wrapper uses double underscore to traverse relationships
    else:
        cartItems = order['get_cart_items']
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context= {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cartItems = order['get_cart_items']
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
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




zxcvbnmzxcvbnmxcvbnm