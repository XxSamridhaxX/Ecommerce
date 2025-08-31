import json
from .models import Product,Order

def cookieCart(request):
    # If cookie exists
    try:
        cart = json.loads(request.COOKIES['cart'])
        # if first time visits and no cookie exists
    except:
        cart = {}
        print(cart)

        # Empty items list for anonymous users
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
            # We're enclosing this inside try catch because cookie ma bhako item db bata delete pani bhaisakeko huncha so 
            # product bhanera nikalda reference error dera no item exists bhanne error auna sakcha so try except block ma haleko eslai
            # Problem: DoesNotExist at /cart/
        try:
            product = Product.objects.get(id = i)
            total = (product.price*cart[i]['quantity'])

            # for over all total add total of each items
            order['get_cart_total']+=total
            cartItems += cart[i]['quantity']
            order['get_cart_items']= cartItems

            # For each item in our Cookiecart
            item = {
                        'product':
                            {
                                'id':product.id,
                                'name':product.name, 
                                'ImageURL': product.ImageURL,
                                'price':product.price,
                            },
                            'quantity':cart[i]['quantity'],
                            'get_total':total,

                    }
            items.append(item)

            if product.digital == "False":
                order['shipping'] = True

        except:
            pass
    
    return {'items':items,'order':order,'cartItems':cartItems}

def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return {'items':items, 'order':order, 'cartItems':cartItems}