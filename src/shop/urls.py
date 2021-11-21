from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('status', views.status, name='status'),
  path('product/<slug>', views.product, name='product'),
  path('contact', views.contact, name='contact'),
  path('collections', views.collections, name='collections'),
  path('collections/<slug>', views.collection, name='collection'),
  path('cart', views.cart, name='cart'),
  path('wishlist', views.wishlist, name='wishlist'),
  path('checkout', views.checkout, name='checkout'),
  path('404', views.error404, name='404'),
]
