from django import forms
from .models import Producto
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