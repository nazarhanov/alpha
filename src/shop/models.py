from django.db import models
from django.db.models import fields


class Group(models.Model):
  name = models.CharField(max_length=255)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)


class SingleField(models.Model):
  name = models.CharField(max_length=255, unique=True)
  key = models.CharField(max_length=255, blank=True)
  value = models.CharField(max_length=1023, blank=True)
  created_date = models.DateField(auto_now_add=True)
  updated_date = models.DateField(auto_now=True)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)


class MultiField(models.Model):
  name = models.CharField(max_length=255)
  key = models.CharField(max_length=255, blank=True)
  value = models.CharField(max_length=1023, blank=True)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Category(models.Model):
  name = models.CharField(max_length=255)
  slug = models.CharField(max_length=255, unique=True)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)
  parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

  class Meta:
    verbose_name_plural = "Categories"

  def __str__(self):
    return self.name


class Tag(models.Model):
  name = models.CharField(max_length=255)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)


class Size(models.Model):
  name = models.CharField(max_length=255)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)


class Color(models.Model):
  name = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)


class Product(models.Model):
  name = models.CharField(max_length=255)
  short_desc = models.CharField(max_length=255) 
  full_desc = models.TextField()
  price = models.DecimalField(max_digits=11, decimal_places=2)
  views = models.BigIntegerField(default=0)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)
  categories = models.ManyToManyField(Category)
  tags = models.ManyToManyField(Tag)
  sizes = models.ManyToManyField(Size)
  colors = models.ManyToManyField(Color)
  slug = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.name


class Image(models.Model):
  name = models.CharField(max_length=2047)
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  color = models.ForeignKey(Color, on_delete=models.CASCADE)


class Review(models.Model):
  author = models.CharField(max_length=255) 
  content = models.CharField(max_length=1023)
  photo = models.CharField(max_length=2047) 
  email = models.EmailField(max_length=319) 
  rating = models.BigIntegerField(default=0) 
  created_date = models.DateField(auto_now_add=True) 
  updated_date = models.DateField(auto_now=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
