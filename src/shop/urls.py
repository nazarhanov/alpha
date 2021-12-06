from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('status', views.status, name='status'),
  path('products/<slug>', views.product, name='products'),
  path('contact', views.contact, name='contact'),
  path('collections', views.collection, name='collections'),
  path('collections/<slug>', views.collection, name='collections'),
  path('cart', views.cart, name='cart'),
  path('cart/add/<id>', views.add_to_cart, name='add_to_cart'),
  path('cart/remove/<id>', views.remove_from_cart, name='remove_from_cart'),
  path('wishlist', views.wishlist, name='wishlist'),
  path('wishlist/add/<id>', views.add_to_wishlist, name='add_to_wishlist'),
  path('wishlist/remove/<id>', views.remove_from_wishlist, name='remove_from_wishlist'),
  path('checkout', views.checkout, name='checkout'),
  path('thanks', views.thanks, name='thanks'),
  path('404', views.error_404, name='404'),
]
