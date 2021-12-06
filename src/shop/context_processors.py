from shop.models import Category
from shop.cart import Cart
from shop.wishlist import Wishlist

def categories(request):
  objects = Category.objects.all()

  categories = []
  subcategories = {}

  for category in objects:
    item = {
      'id': category.id,
      'name': category.name,
      'slug': category.slug,
    }

    if category.parent:
      if subcategories.get(category.parent_id):
        subcategories[category.parent_id].append(item)
      else:
        subcategories[category.parent_id] = [item]
    else:
      categories.append(item)

  for category in categories:
    if subcategories.get(category['id']):
      category['sub'] = subcategories[category['id']]

  return {
    'categories': categories
  }

def cart(request):
  cart = Cart(request)

  return {
    'cart': cart
  }

def wishlist(request):
  wishlist = Wishlist(request)

  return {
    'wishlist': wishlist
  }
