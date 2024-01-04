from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart,cartData ,guestOrder

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products =Product.objects.all()
    context ={'products':products ,'cartItems':cartItems }
    return render(request , 'store/store.html',context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items ,'order': order,'cartItems':cartItems ,'shipping':False}
    return render(request , 'store/cart.html' ,context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items ,'order': order, 'cartItems':cartItems}
    return render(request ,'store/checkout.html',context)

def updateItem(request):
    #從請求的主體（body）中解析 JSON 數據
    data = json.loads(request.body)
    productId = data['productId']
    action =data['action']

    print('Action:',action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, create = Order.objects.get_or_create(customer= customer, complete=False)

    orderItem,create = OrderItem.objects.get_or_create(order=order ,product=product)

    if action =='add':
        orderItem.quantity+=1
    elif action =='remove':
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('Item was added' ,safe=False) 

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer= customer, complete=False)      

    else:
        customer,order =  guestOrder(request,data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],

        )
    print(data)
    '''
    ex:
    {'form': {'name': None, 'email': None, 'total': '14.99'}, 
     'shipping': {'address': '360.st', 'city': 'tap', 'state': 'ta', 'zipcode': '88', 'country': 'tap'}}
    '''

    return JsonResponse('Payment Complete', safe=False)

def pages(request,name):
    data = cartData(request)
    
    cartItems = data['cartItems']

    products =Product.objects.get(name=name)
    context ={'products':products ,'cartItems':cartItems}
    return render(request , 'store/pages.html',context)
    

# Create your views here.
