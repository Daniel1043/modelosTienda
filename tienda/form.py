from django import forms
from .models import Producto,Compra,Marca
from django.contrib.auth.forms import AuthenticationForm

class cambiarProducto(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['vip','precio','unidades','modelo','nombre','marca']




class iniciar_sesion(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Usuario",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
            }
        )
    )
    next = forms.CharField(widget=forms.HiddenInput, initial="/")
    
    
    
class comprasForm(forms.ModelForm):
     class Meta:
        model = Compra
        fields = ['unidades']




class fitroForm(forms.Form):
    nombre = forms.CharField(required=False,widget=forms.TextInput({"placeholder": "Buscar. . ."}))
    marca = forms.ModelMultipleChoiceField(queryset=Marca.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    
    