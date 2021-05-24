from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages





def registerPage(request):
   form = CreateUserForm()

   if request.method == 'POST':
     form = CreateUserForm(request.POST)
     if form.is_valid():
       user = form.save()
       username = form.cleaned_data.get('username')
       #group = Group.objects.get(name='customer')
       #user.groups.add(group)
       Customer.objects.create(
           user=user,
       )

       messages.success(
           request, 'Account was created successfully for ' + username)
       return redirect('login')

   context = {'form': form}
   return render(request, 'store/register.html', context)
 
 
 def loginPage(request):
  
  if request.method == 'POST':
     username = request.POST.get('username')
     password = request.POST.get('password')
     user = authenticate(request, username = username, password=password)
     
     if user is not None:
        login(request, user)
        return redirect('home')
     else:
       messages.info(request, 'Username or password is incorrect')
       
  context = {}
  return render(request, 'accounts/login.html', context)


def logoutUser(request):
  logout(request)
  return redirect('login')


@login_required(login_url='login')
def home(request):
  orders = Order.objects.all()
  customers =Customer.objects.all()
  
  total_customers = customers.count()
  total_orders =orders.count()
  delivered = orders.filter(status='Delivered').count()
  pending = orders.filter(status='Pending').count()

  
  
  context = {'orders': orders, 'customers': customers, 'total_customers': total_customers, 
             'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
  return render(request, 'accounts/dashboard.html', context)






def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)




def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
  
 if request.method == 'GET':
  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']
  print('Action:', action)
  print('Product:', productId)
	
 customer = request.user.customer
 product = Product.objects.get(id=productId)
 order, created = Order.objects.get_or_create(customer=customer, complete=False)
 
 orderItem, created = OrderItem.objects.get_or_create(
		order=order, product=product)
 
 if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
 elif action == 'remove':
   orderItem.quantity = (orderItem.quantity - 1)
	
 orderItem.save()
 if orderItem.quantity <= 0:
		orderItem.delete()
  
 return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(
			customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

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
                    zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
