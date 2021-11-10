from django.contrib import admin
from . import models  


admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Review)
admin.site.register(models.Image)
admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Group)
admin.site.register(models.SingleField)
admin.site.register(models.MultiField)
