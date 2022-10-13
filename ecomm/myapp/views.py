from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import *
from .models import *
import json


# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, "shipping": False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'items': items, 'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, "shipping": False}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('user is not logged in')
    return JsonResponse('Payment complete', safe=False)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            fname = request.POST['first_name']
            email = request.POST['email']
            Customer.objects.create(user=user, name=fname, email=email)

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('store')
    else:
        form = SignupForm()
    return render(request, 'accounts/register.html', {'form': form})


def enter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect('store')
        error = messages.warning(request, f'wrong credentials check!!')
        templatename = 'accounts/login.html'
        context = {'error': error}
        return render(request, templatename, context)
    templatename = 'accounts/login.html'
    context = {}
    return render(request, templatename, context)


def getout(request):
    logout(request)
    return redirect('store')

    # -------------------------------------ListView---------------------------


def AdminDashoard(request):
    template_name = 'dashboard.html'
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name, context)

    # -------------------------------------ListView---------------------------

    # -------------------------------------DetailView---------------------------


class productDetailView(DetailView):
    model = Product

    # -------------------------------------DetailView---------------------------


# ---------------------------CreateView---------------------

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'quantity', 'digital', 'status', 'image']

    def form_valid(self, form):
        return super(ProductCreateView, self).form_valid(form)

    # -------------------UpdateView------------------------


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'quantity', 'digital', 'status', 'image']

    def form_valid(self, form):
        return super(ProductUpdateView, self).form_valid(form)


class OrderListView(ListView):
    model = Order
    context_object_name = 'order'
    ordering = ['-date_ordered']
