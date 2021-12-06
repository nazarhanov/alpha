from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models  
from . import signals  


class OrderItemInline(admin.TabularInline):
  model = models.OrderItem

  fields = ['product', 'count', 'color', 'size', 'product_link']
  readonly_fields = ['product_link']

  def product_link(self, obj):
    return mark_safe(f'<a href="https://localhost" target="_blank">View</a>')


class OrderAdmin(admin.ModelAdmin):
  inlines = [
    OrderItemInline,
  ]

  def response_add(self, request, instance, post_url_continue=None):
    signals.order_save.send(sender=models.Order, instance=instance)
    return super().response_add(request, instance, post_url_continue)


admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)
admin.site.register(models.Review)
admin.site.register(models.Image)
admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Group)
admin.site.register(models.SingleField)
admin.site.register(models.MultiField)
