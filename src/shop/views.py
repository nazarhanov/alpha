from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from shop.models import Category, Product, Image, Size
from shop.cart import Cart
from shop.wishlist import Wishlist
from . import models
from . import forms
from . import signals


def index(request):
  products = Product.objects.all().order_by('-views')[:3]

  for product in products:
    product = product.__dict__
    product['image'] = Image.objects.filter(product__id=product['id']).first()

  return render(request, 'shop/pages/index.html', {'products': products})


def product(request, slug):
  context = {}

  instance = get_object_or_404(Product, slug=slug)
  instance.views += 1
  instance.save()

  product = instance.__dict__
  product['category'] = instance.categories.first()
  product['sizes'] = instance.sizes.all()
  product['colors'] = instance.colors.all()

  cart = Cart(request)
  cart = cart.cart
  context['product_in_cart'] = str(product['id']) in cart
  wishlist = Wishlist(request)
  wishlist = wishlist.wishlist
  context['product_in_wishlist'] = str(product['id']) in wishlist

  color = request.GET.get('color', None)
  count = int(request.GET.get('count', 1))
  size = int(request.GET.get('size', product['sizes'][0].id))

  if color:
    product['images'] = Image.objects.filter(product__id=product['id'], color__id=color).all()
    color = int(color)
  else:
    product['images'] = Image.objects.filter(product__id=product['id'], color__id=product['colors'][0].id).all()
    color = product['colors'][0].id

  state = {
    'size': size,
    'color': color,
    'count': count,
  }

  context['product'] = product
  context['state'] = state
  context['counts'] = range(1, 7)
  return render(request, 'shop/pages/product.html', context)


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
    'sort': request.GET.get('sort', '1'),
    'count': request.GET.get('count', '1'),
    'search': request.GET.get('search', ''),
    'page': int(request.GET.get('page', 1)),
  }

  if slug == 'all':
    products = Product.objects.filter(name__icontains=query['search'])
    category = {
      'name': 'Collections',
      'slug': slug,
    }
  else:
    category = get_object_or_404(Category, slug=slug).__dict__
    subcategories = Category.objects.filter(parent__id=category['id'])
    categories = [category['id']] + [sub.id for sub in subcategories]
    products = Product.objects.filter(categories__id__in=categories)

  if query['sort'] and query['sort'] != '1':
    products = products.order_by(sorts[query['sort']])

  paginator = Paginator(products, counts[query['count']] if query['count'] in counts else counts['1']) 

  page = request.GET.get('page')
  page = paginator.get_page(page)
  products = list(page)

  cart = Cart(request)
  cart = cart.cart
  wishlist = Wishlist(request)
  wishlist = wishlist.wishlist

  for i in range(0, len(products)):
    product = products[i].__dict__
    product['image'] = Image.objects.filter(product__id=product['id']).first()
    product['in_cart'] = str(product['id']) in cart
    product['in_wishlist'] = str(product['id']) in wishlist
    products[i] = product

  state = {
    'category': {
      'name': category['name'],
      'slug': category['slug'],
    },
  }

  return render(request, 'shop/pages/collections.html', {'page': page, 'state': state, 'query': query})


def cart(request):
  context = {}
  instance = Cart(request)
  cart = instance.cart

  products = []

  for product in instance.products():
    pinstance = product
    product = product.__dict__

    key = str(product['id'])
    cproduct = cart[key]

    product['image'] = Image.objects.filter(
      product__id=key,
      color__id=cproduct['color']
    ).first()
    product['count'] = cproduct['count']
    product['total'] = pinstance.total(product['count'])
    product['params'] = cproduct

    products.append(product)

  context['products'] = products
  context['total'] = instance.total()

  return render(request, 'shop/pages/cart.html', context)


def add_to_cart(request, id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=id)

  params = {
    'color': request.GET.get('color', None),
    'count': request.GET.get('count', 1),
    'size': request.GET.get('size', None),
  }

  if not params['color']:
    params['color'] = product.colors.first().id

  if not params['size']:
    params['size'] = product.sizes.first().id

  cart.add(id, params)

  return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, id):
  cart = Cart(request)

  cart.remove(id)

  return redirect(request.META.get('HTTP_REFERER'))


def wishlist(request):
  context = {}
  instance = Wishlist(request)
  wishlist = instance.wishlist

  products = []

  for product in instance.products():
    pinstance = product
    product = product.__dict__

    key = str(product['id'])
    cproduct = wishlist[key]

    cart = Cart(request)
    cart = cart.cart

    product['image'] = Image.objects.filter(
      product__id=key,
      color__id=cproduct['color']
    ).first()
    product['count'] = cproduct['count']
    product['total'] = pinstance.total(product['count'])
    product['params'] = cproduct
    product['in_cart'] = str(product['id']) in cart

    products.append(product)

  context['products'] = products
  context['total'] = instance.total()

  return render(request, 'shop/pages/wishlist.html', context)


def add_to_wishlist(request, id):
  wishlist = Wishlist(request)
  product = get_object_or_404(Product, id=id)

  params = {
    'color': request.GET.get('color', None),
    'count': request.GET.get('count', 1),
    'size': request.GET.get('size', None),
  }

  if not params['color']:
    params['color'] = product.colors.first().id

  if not params['size']:
    params['size'] = product.sizes.first().id

  wishlist.add(id, params)

  return redirect(request.META.get('HTTP_REFERER'))


def remove_from_wishlist(request, id):
  wishlist = Wishlist(request)

  wishlist.remove(id)

  return redirect(request.META.get('HTTP_REFERER'))


def checkout(request):
  context = {}
  instance = Cart(request)
  cart = instance.cart
  cproducts = instance.products()

  if not len(cproducts):
    return redirect('404')

  products = []

  for product in cproducts:
    pinstance = product
    product = product.__dict__

    key = str(product['id'])
    cproduct = cart[key]

    product['instance'] = pinstance
    product['color'] = cproduct['color']
    product['size'] = cproduct['size']
    product['count'] = cproduct['count']
    product['total'] = pinstance.total(product['count'])

    products.append(product)

  context['products'] = products

  if request.method == 'POST':
    form = forms.OrderForm(request.POST)

    if form.is_valid():
      order = form.save(commit=False)
      order.save()

      order_items = []

      for product in products:
        order_items.append(
          models.OrderItem(
            product=product['instance'],
            order=order, 
            count=product['count'], 
            color=models.Color.objects.filter(id=product['color']).first(), 
            size=models.Size.objects.filter(id=product['size']).first(),
          )
        )

      models.OrderItem.objects.bulk_create(order_items)

      signals.order_save.send(sender=models.Order, instance=order)
      instance.clear()

      return render(None, 'shop/pages/thanks.html')

  else:
    form = forms.OrderForm(initial={'payment': '1'})

  context['form'] = form
  context['total'] = instance.total()

  return render(request, 'shop/pages/checkout.html', context)


def thanks(request):
  response = render(None, 'shop/pages/thanks.html')
  return response


def status(request):
  if request.method == 'POST':
    return JsonResponse({'status': 'ok'})

  return redirect('404')


def error_404(request, *args, **argv):
  response = render(None, 'shop/pages/404.html')
  response.status_code = 404
  return response
