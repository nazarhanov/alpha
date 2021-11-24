from django import template

register = template.Library()

@register.simple_tag
def urlquery(params, key=None, value=None):
  '''Converts dict to query string'''
  params = dict(params)
  
  if key:
    params[key] = value

  return '&'.join(x + '=' + str(y) for x, y in params.items())
