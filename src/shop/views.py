from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
from shop.models import Category

def index(request):
  return render(request, 'shop/pages/index.html')

def product(request, slug):
  return render(request, 'shop/pages/product.html')

def contact(request):
  return render(request, 'shop/pages/contact.html')

def collections(request):
  return render(request, 'shop/pages/collections.html')

def collection(request, slug):
  return render(request, 'shop/pages/collections.html')

def cart(request):
  return render(request, 'shop/pages/cart.html')

def wishlist(request):
  return render(request, 'shop/pages/wishlist.html')

def checkout(request):
  return render(request, 'shop/pages/checkout.html')

def status(request):
  if request.method == 'POST':
    return JsonResponse({'status': 'ok'})

  return redirect('/404')

def error404(request, *args, **argv):
  response = render(None, 'shop/pages/404.html')
  response.status_code = 404
  return response
