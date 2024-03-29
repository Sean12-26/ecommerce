import json
from .models import *


def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart={}
    print('cart:',cart)
    items=[]
    order = {'get_cart_total':0 ,'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:       #例外處理，購物車裡的商品被刪除時自動從購物車裡移除
            cartItems += cart[i]['quantity'] #購物車圖標數量

            product = Product.objects.get(id=i)
            total =(product.price * cart[i]['quantity'] )

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item={
                'product':{   
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL},

                'quantity': cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return{'cartItems':cartItems, 'order':order, 'items':items}



def cartData(request):
    if  request.user.is_authenticated:
        customer  = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer ,complete=False)
        items =order.orderitem_set.all()
        cartItems = order.get_cart_items #購物車內商品總數
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return{'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request,data):
#    print('requset:',request)
    print('User is not logged in')
#    print('COOKIES:', request.COOKIES)
#    print('data:',data)
    name = data['form']['name']
    email =data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    print('items:',items)

    customer, created =Customer.objects.get_or_create(email=email)
    customer.name =name
    customer.save()
    print('customer:',customer)
    order = Order.objects.create(customer=customer, complete=False)
    print('order:',order)

    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = (item['quantity'] if item['quantity']>0 else -1*item['quantity'])
        )

    return customer,order