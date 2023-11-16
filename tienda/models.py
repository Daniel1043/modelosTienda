from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Marca(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Marcas"

        
class Producto(models.Model):
    vip = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(limit_value=0)])
    unidades = models.PositiveIntegerField()
    modelo = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
   

    def __str__(self):
        return f'{self.marca} {self.modelo}'
    
    class Meta:
        unique_together =['marca','modelo']
        verbose_name_plural = "Productos"



   




class Cliente(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saldo=models.DecimalField(max_digits=12, decimal_places=2)
    vip=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'
    
    class Meta:
        verbose_name_plural = "Clientes"


class Compra(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    user=models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.IntegerField()
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0.21)
    
    def __str__(self):
        return f'{self.user.user.username}{self.fecha}'
    
    class Meta:
        unique_together=['fecha', 'producto', 'user']
        verbose_name_plural="Compras"
    
