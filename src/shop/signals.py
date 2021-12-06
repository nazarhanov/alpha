import os
import requests
from django.contrib.sites.models import Site
from django.dispatch import receiver, Signal
from django import template
from . import models  


order_save = Signal()


def format_message(order, items):
  products = ''
  index = 1
  total = 0
  domain = Site.objects.get(id=1).domain

  for item in items:
      product = item.product
      
      link = domain + "{% load poll_extras %}{% url 'products' slug=product.slug %}?{% urlquery params %}"
      t = template.Template(link)
      c = template.Context({
        'product': product, 
        'params': {
          'count': item.count,
          'color': item.color.id,
          'size': item.size.id,
        }
      })
      link = t.render(c)

      products += f'{index}. [{product.name}]({link}):\n'
      products += f'    = ${product.price} × {item.count} = ${product.price * item.count}\n'
      index += 1
      total += product.price * item.count 

  products = products.strip()

  return f'''
[📦 ORDER #{order.id}](https://{domain}/admin/shop/order/{order.id}/change/)
————————————
{products}

📌 TOTAL: {total}
'''.strip()


@receiver(order_save, sender=models.Order)
def notify_telegram_chat(sender, instance, **kwargs):
  order_items = instance.orderitem_set.all()

  params = {
    'chat_id': '-715345299', 
    'text': format_message(instance, order_items),
    'parse_mode': 'Markdown',
  }

  response = requests.post(f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/sendMessage', params=params)
