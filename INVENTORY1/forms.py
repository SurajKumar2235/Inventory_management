from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Inventory,Category

class UserRegistration(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']



class InventoryForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=Category.objects.all(),initial=0)
    class Meta:
        model=Inventory
        fields=['name','quantity','category']


from django import forms

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})

    class Meta:
        model = Inventory
        fields = ['name', 'quantity']