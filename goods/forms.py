from django import forms
from django.forms import CheckboxSelectMultiple
from .models import *

class GoodsForm(forms.ModelForm):
    class Meta:
        model  = Goods
        exclude = ('user','epq')

        widgets = {
            'raw_material': CheckboxSelectMultiple(),
        }
        
    
    def clean_name(self):
        name = self.cleaned_data.get('good_name').upper()
        return name

    def __init__(self,user=None,*args,**kwargs):
        super(GoodsForm,self).__init__(*args,**kwargs)
        if user:
            self.fields['raw_material'].queryset=Product.objects.filter(user=user) 