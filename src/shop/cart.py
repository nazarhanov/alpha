from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
  def __init__(self, request):
    self.session = request.session
    cart = self.session.get(settings.CART_SESSION_ID)

    if not cart:
      cart = self.session[settings.CART_SESSION_ID] = {}

    self.cart = cart

  def products():
    return self.cart

  def save(self):
    self.session[settings.CART_SESSION_ID] = self.cart
    self.session.modified = True

  def add(self, id, params):
    if not self.cart.get(str(id), False):
      self.cart[str(id)] = {}

    params['count'] = int(params.get('count', 0))
    self.cart[str(id)] = params
    self.save()

  def remove(self, id):
    if not self.cart.get(str(id), False):
      return

    del self.cart[str(id)]
    self.save()

  def __iter__(self):
    product_ids = self.cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    for product in products:
      yield product

  def products(self):
    product_ids = self.cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    return products

  def __len__(self):
    return sum(item['count'] for item in self.cart.values())

  def total(self):
    total = 0

    for product in self:
      count = self.cart[str(product.id)]['count']
      total += product.total(count)

    return total

  def clear(self):
    del self.session[settings.CART_SESSION_ID]
    self.session.modified = True
