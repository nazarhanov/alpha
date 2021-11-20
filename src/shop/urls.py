from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('status', views.status, name='status'),
  path('product/<slug>', views.product, name='product'),
  path('contact', views.contact, name='contact'),
  path('collections/<slug>', views.collections, name='collections'),
  path('cart', views.cart, name='cart'),
  path('wishlist', views.wishlist, name='wishlist'),
  path('checkout', views.checkout, name='checkout'),
  path('404', views.error404, name='404'),
]
