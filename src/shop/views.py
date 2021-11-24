from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from shop.models import Category, Product, Image, Size
from shop.cart import Cart

def index(request):
  products = Product.objects.all().order_by('-views')[:3]

  for product in products:
    product = product.__dict__
    product['image'] = Image.objects.filter(product__id=product['id']).first()

  return render(request, 'shop/pages/index.html', {'products': products})

def product(request, slug):
  instance = get_object_or_404(Product, slug=slug)
  instance.views += 1
  instance.save()

  product = instance.__dict__
  product['category'] = instance.categories.first()
  product['sizes'] = Size.objects.filter(product__id=product['id'])
  product['colors'] = instance.colors.all()

  size = request.GET.get('size')
  color = request.GET.get('color')

  if color:
    product['images'] = Image.objects.filter(product__id=product['id'], color__id=color).all()
    color = int(color)
  else:
    product['images'] = Image.objects.filter(product__id=product['id'], color__id=product['colors'][0].id).all()
    color = product['colors'][0].id
  
  if size:
    size = int(size)
  else:
    size = product['sizes'][0].id

  state = {
    'size': size,
    'color': color,
  }

  return render(request, 'shop/pages/product.html', {'product': product, 'state': state})

def contact(request):
  return render(request, 'shop/pages/contact.html')

counts = {
  '1': 12,
  '2': 24,
  '3': 36,
}

sorts = {
  '1': 'default',
  '2': 'name',
  '3': 'price',
}

def collection(request, slug='all'):
  query = {
    'sort': request.GET.get('sort') or '1',
    'count': request.GET.get('count') or '1',
    'search': request.GET.get('search') or '',
  }

  if slug == 'all':
    products = Product.objects.filter(name__icontains=query['search'])
    category = {
      'name': 'Collections',
      'slug': slug,
    }
  else:
    category = get_object_or_404(Category, slug=slug).__dict__
    products = Product.objects.filter(categories__id=category['id'])

  if query['sort'] and query['sort'] != '1':
    products = products.order_by(sorts[query['sort']])

  paginator = Paginator(products, counts[query['count']] if query['count'] in counts else counts['1']) 

  page = request.GET.get('page')
  page = paginator.get_page(page)
  products = list(page)

  for i in range(0, len(products)):
    products[i] = products[i].__dict__
    products[i]['image'] = Image.objects.filter(product__id=products[i]['id']).first()

  state = {
    'category': {
      'name': category['name'],
      'slug': category['slug'],
    },
  }

  return render(request, 'shop/pages/collections.html', {'page': page, 'state': state, 'query': query})

def cart(request):
  cart = Cart(request)
  cart = cart.cart

  products = []

  for id in cart.keys():
    product = Product.objects.filter(id=id).first()
    product = product.__dict__
    product['image'] = Image.objects.filter(product__id=product['id']).first()
    products.append(product)

  return render(request, 'shop/pages/cart.html', {'products': products})

def add_to_cart(request, id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=id)

  query = {
    'count': request.GET.get('count') or 1,
  }

  query['count'] = int(query['count'])

  cart.add(
    product=product,
    count=query['count'],
  )

  return redirect(request.META.get('HTTP_REFERER'))

def remove_from_cart(request, id):
  cart = Cart(request)

  cart.remove(id)

  return redirect(request.META.get('HTTP_REFERER'))

def wishlist(request):
  return render(request, 'shop/pages/wishlist.html')

def checkout(request):
  return render(request, 'shop/pages/checkout.html')

def status(request):
  if request.method == 'POST':
    return JsonResponse({'status': 'ok'})

  return redirect('/404')

def error_404(request, *args, **argv):
  response = render(None, 'shop/pages/404.html')
  response.status_code = 404
  return response
