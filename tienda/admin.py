from django.contrib import admin
from .models import Marca,Producto,Compra,Cliente

admin.site.register(Cliente)
admin.site.register(Marca)
admin.site.register(Compra)
admin.site.register(Producto)


