from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from .utils import cart_data, guest_order

# Create your views here.
def store(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    p = Product.objects.all()
    return render(request, 'store/store.html', {'products': p, 'cart_items': cart_items})

def cart(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    return render(request, 'store/cart.html', {'items':items, 'order':order, 'cart_items': cart_items})

def checkout(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    return render(request, 'store/checkout.html', {'items':items, 'order':order, 'cart_items': cart_items})

@csrf_exempt
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added to cart', safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(transaction_id)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'])
    return JsonResponse('Order proccessed...', safe=False)
