from django.shortcuts import render
from django.http import JsonResponse
import datetime
import json
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RateForm
from .models import Product,Orderitem,Category,Subcategory,Order,Rating
from django.urls import reverse
from django.db.models import Avg
from .filters import ProductFilter



# Create your views here.
def store (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(name__icontains=q)
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    # if categoryID:
    #     products = Product.objects.filter(subcategory=categoryID)
    # else:
    #     products = Product.objects.all()

    if request.user.is_authenticated:
        user=request.user
        transaction_id=datetime.datetime.now().timestamp()
        order ,created = Order.objects.get_or_create(user=user,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartItems= order['get_cart_items']
    # myFilter = ProductFilter(request.GET, queryset=products)
    # products= myFilter.qs
    context ={'products':products,
    'categories':categories,
    'cartItems':cartItems,
    # 'myFilter': myFilter,
    }
    return render (request,'fashionz/store.html',context)


@login_required
def ProductDetail(request, pk):
    product = Product.objects.get(id=pk)
    ratings = Rating.objects.filter(product=product)
    average_ratings = ratings.aggregate(Avg('rate'))
    total_ratings = ratings.count()
    context = {
        'product': product,
        'average_ratings': average_ratings,
        'ratings': ratings,
        'total_ratings': total_ratings,
    }
    return render(request, 'fashionz/details.html', context)


@login_required
def Rate(request, pk):
    # getting post objects by their id
    product = Product.objects.get(id=pk)
    user = request.user
    # form method
    if request.method == 'POST':
        form = RateForm(request.POST)
        # validating the form.
        if form.is_valid():
            rate = form.save()
            rate.product = product
            rate.user = user
            rate.save()
            return HttpResponseRedirect(reverse('detail', args=[pk]))
    else:
        form = RateForm()
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'fashionz/rate.html', context)

def cart (request):
    if request.user.is_authenticated:
        user = request.user
        order ,created = Order.objects.get_or_create(user=user,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems= order['get_cart_items']

    context ={'items':items,'order':order,'cartItems': cartItems}
    return render (request,'fashionz/cart.html',context)

def checkout (request):
    if request.user.is_authenticated:
        user = request.user
        order ,created = Order.objects.get_or_create(user=user,complete=False)
        items = order.orderitem_set.all()

    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}


    context ={'items':items,'order':order}
    return render (request,'fashionz/checkout.html',context)
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action', action)
    print('ProductId', productId)
    user = request.user
    product=Product.objects.get(id=productId)
    order ,created = Order.objects.get_or_create(user=user,complete=False)
    orderItem, created=Orderitem.objects.get_or_create(order=order,product=product)#change quantity
    if action == 'add':
        orderItem.quantity=(orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)
def processOrder(request):
    # print('Data:',request.body)
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        user=request.user
        order, created=Order.objects.get_or_create(user=user,complete=False)
        total=float(data['form']['total'])

        order.transaction_id= transaction_id

        final_total=order.get_cart_total/100

        # if total == order.get_cart_total:
        if total ==final_total:
            order.complete=True
        order.save()
    else:
        print('User is not logged in')

        alert('Please log in first to use the cart')
    return JsonResponse('Payment Complete!!',safe=False)
