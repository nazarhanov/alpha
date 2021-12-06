from django import forms
from . import models


class OrderForm(forms.ModelForm):

  class Meta:
    model = models.Order
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'comment', 'payment']

    widgets = {
      'first_name': forms.TextInput(attrs={'placeholder': 'First Name*' }),
      'last_name': forms.TextInput(attrs={'placeholder': 'Last Name*' }),
      'email': forms.TextInput(attrs={'placeholder': 'Email*' }),
      'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number*' }),
      'comment': forms.Textarea(attrs={'placeholder': 'Comment*', 'cols': 8, 'rows': 3 }),
      'payment': forms.RadioSelect(),
    }

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    comment = forms.CharField(required=False)
    payment = forms.ChoiceField(choices=models.Order.PAYMENT_CHOICES)
    # comment = forms.CharField(required=True)
