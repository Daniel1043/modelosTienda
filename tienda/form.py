from django import forms
from .models import Producto

class cambiarProducto(forms.ModelForm):


    class Meta:
        model = Producto
        fields = ['vip','precio','unidades','modelo','nombre','marca']



