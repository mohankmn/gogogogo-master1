from django import forms
from .models import Purchase, Product
from os import name
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.http import request


class PurchaseForm(forms.ModelForm):
    class Meta:
        model  = Purchase
        fields = ['product', 'quantity', 'price', 'recieved', 'date']

    def __init__(self,user=None,*args,**kwargs):
        super(PurchaseForm,self).__init__(*args,**kwargs)
        if user:
            self.fields['product'].queryset=Product.objects.filter(user=user)

class ItemsForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name','average_daily_demand','unit_costprice','carrying_cost','ordering_cost','total_inventory','lead_time','service_level','standard_deviation','no_of_workingdays']

    def clean_name(self):
        name = self.cleaned_data.get('name').upper()
        return name

class ItemSearchForm(forms.ModelForm):
   class Meta:
        model = Product
        fields = ['name']

class select_item(forms.ModelForm):
    class Meta:
        model  = Purchase
        fields = ['product']
        

    def __init__(self,user=None,*args,**kwargs):
        super(select_item,self).__init__(*args,**kwargs)
        if user:
            self.fields['product'].queryset=Product.objects.filter(user=user)