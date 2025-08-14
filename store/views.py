from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.db.models import F,ExpressionWrapper, FloatField
# Create your views here.

def store(request):
    products = Product.objects.all()
    context= {'products':products}
    return render(request,'store/store.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        # items = items.annotate(total = ExpressionWrapper(F('quantity')*F('product__price'),output_field=FloatField()))
        # Expression wrapper uses double underscore to traverse relationships
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context= {'items':items,'order':order}
    return render(request,'store/cart.html',context)


def checkout(request):
    context= {}
    return render(request,'store/checkout.html',context)
