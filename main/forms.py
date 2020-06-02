from django import forms
from django.forms import ModelForm
from .models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields=['title','cost','image','description','quantity']