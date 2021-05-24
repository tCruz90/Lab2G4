from django.shortcuts import render

# Create your views here.

def store(request):
  context={}
  return render(request, 'store/store.hmtl', context)


def cart(request):
  context = {}
  return render(request, 'store/cart.hmtl', context)


def checkout(request):
  context = {}
  return render(request, 'store/checkout.hmtl', context)
