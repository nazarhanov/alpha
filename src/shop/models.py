from django.db import models
from django.db.models import fields
from django.core.validators import RegexValidator


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

  def total(self, count=1):
    return self.price * count


class Order(models.Model):
  first_name = models.CharField(max_length=255, blank=False)
  last_name = models.CharField(max_length=255, blank=False)
  email = models.EmailField(max_length=319, blank=False)
  phone_number = models.CharField(max_length=255, blank=False, validators=[
    RegexValidator(
      regex=r'^\d{7,15}$',
      message='Phone number must contain only nums. Up to 15 digits allowed.',
    ),
  ])
  comment = models.CharField(max_length=1023, blank=True)
  products = models.ManyToManyField(Product, through='OrderItem')

  PAYMENT_CHOICES = (
    ('1', 'Cash'),
    ('2', 'Card'),
  )

  payment = models.CharField(max_length=255, blank=False, choices=PAYMENT_CHOICES, default='Cash')
  closed = models.BooleanField(default=False, blank=False)

  def __str__(self):
    return f"#{self.id}  {self.first_name} {self.last_name} - {'Processing' if not self.closed else 'Closed'}"


class OrderItem(models.Model):
  product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE)
  order = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE)
  count = models.BigIntegerField(default=1, blank=False)
  color = models.ForeignKey(Color, blank=False, on_delete=models.CASCADE)
  size = models.ForeignKey(Size, blank=False, on_delete=models.CASCADE)


class Image(models.Model):
  url = models.CharField(max_length=2047)
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
