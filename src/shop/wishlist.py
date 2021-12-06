from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Wishlist(object):
  def __init__(self, request):
    self.session = request.session
    wishlist = self.session.get(settings.WISHLIST_SESSION_ID)

    if not wishlist:
      wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}

    self.wishlist = wishlist

  def products():
    return self.wishlist

  def save(self):
    self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
    self.session.modified = True

  def add(self, id, params):
    if not self.wishlist.get(str(id), False):
      self.wishlist[str(id)] = {}

    params['count'] = int(params.get('count', 0))
    self.wishlist[str(id)] = params
    self.save()

  def remove(self, id):
    if not self.wishlist.get(str(id), False):
      return

    del self.wishlist[str(id)]
    self.save()

  def __iter__(self):
    product_ids = self.wishlist.keys()
    products = Product.objects.filter(id__in=product_ids)

    for product in products:
      yield product

  def products(self):
    product_ids = self.wishlist.keys()
    products = Product.objects.filter(id__in=product_ids)

    return products

  def __len__(self):
    return sum(item['count'] for item in self.wishlist.values())

  def total(self):
    total = 0

    for product in self:
      count = self.wishlist[str(product.id)]['count']
      total += product.total(count)

    return total

  def clear(self):
    del self.session[settings.WISHLIST_SESSION_ID]
    self.session.modified = True
