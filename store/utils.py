import json
from .models import *


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cart_items = order['get_cart_items']

        for i in cart:
            try:
                cart_items += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = product.price * cart[i]['quantity']
                order['get_cart_items'] += cart[i]['quantity']
                order['get_cart_total'] += total

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'image_url': product.image_url
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
    return {'items':items, 'order':order, 'cart_items': cart_items}

def guest_order(request, data):
    print('user is not logged in')
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cart_data(request)
    items = cookie_data['items']
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for i in items:
        product = Product.objects.get(id=i['product']['id'])
        orderItem = OrderItem.objects.create(product=product, order=order, quantity=i['quantity'])
    return customer, order
