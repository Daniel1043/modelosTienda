from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Cliente, Compra
from django.contrib.admin.views.decorators import staff_member_required
from .form import cambiarProducto, iniciar_sesion, fitroForm, comprasForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum




#Esto enlazara con la pagina de inicio
def welcome(request):
    return render(request,'tienda/index.html', {})

def info(request):
    productos=Producto.objects.all()
    filtro_prod=fitroForm()

    if request.method == "POST":
        filtro_prod = fitroForm(request.POST)
        if filtro_prod.is_valid():
            nombre= filtro_prod.cleaned_data['nombre']
            marca =filtro_prod.cleaned_data['marca']
            
            productos = productos.filter(nombre__contains=nombre)
            if marca:
                productos= productos.filter(marca__id__in=marca)

    form = comprasForm()
    return render(request,'tienda/info.html', {'Productos':productos,'filtro_prod':filtro_prod,'form':form})

#Enlazara con la pagina tienda y mostrara una lista de los productos que ya existen
def tienda(request):
    productos=Producto.objects.all()
    form = comprasForm()
    filtro_prod=fitroForm()

    if request.method == "POST":
        filtro_prod = fitroForm(request.POST)
        if filtro_prod.is_valid():
            nombre= filtro_prod.cleaned_data['nombre']
            marca =filtro_prod.cleaned_data['marca']
            
            productos = productos.filter(nombre__contains=nombre)
            if marca:
                productos= productos.filter(marca__id__in=marca)

    return render(request, 'tienda/tienda.html', {'Productos':productos,'form':form,'filtro_prod':filtro_prod})



@login_required(login_url='loge_ins')
@staff_member_required
#Similar al anterior, mostrara todos los productos que ya existen
def productos(request):
    
        Productos=Producto.objects.filter()
        return render(request, 'tienda/producto.html', {'Productos':Productos})
    

@login_required(login_url='loge_ins')
@staff_member_required
#Te permitira editar los productos ya existentes
def editarProducto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = cambiarProducto(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('productos')
    else:
        form = cambiarProducto(instance=producto)
    return render(request, 'tienda/editar.html', {'form': form, 'pk':pk})


@login_required(login_url='loge_ins')
@staff_member_required
#Te permitira eliminar los productos ya existentes
def eliminarProducto(request, pk):
    producto=Producto.objects.filter(pk=pk).delete()
    return redirect('productos')


@login_required(login_url='loge_ins')
@staff_member_required
#Te permite añadir un nuevo producto
def añadirProducto(request):
    if request.method == "POST":
        form = cambiarProducto(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = cambiarProducto()
    return render(request, 'tienda/nuevo.html', {'form': form})



#Podremos buscar un producto por su nombre
def buscar(request):
    buscar = request.GET.get("producto_buscar")
    nombre = Producto.objects.filter(nombre=buscar)
    return render(request, 'tienda/busqueda.html', {'nombre': nombre, 'buscar':buscar})



#Iniciaremos sesion
def loge_ins(request):
        form = iniciar_sesion()
        template = 'tienda/iniciarSesion.html'
        return_render = render(request, template, {'form': form})
        
        if request.method == "POST":
           
            form = iniciar_sesion(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                next_ruta = request.GET.get('next')
               
                
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                   

                    return_render = redirect(next_ruta)    
                    login(request, user)
                    return return_render

        else:                      
            return return_render



def cerrar_sesion_view(request):
    logout(request)
    return redirect('welcome')


def cliente_check(user):
    return Cliente.objects.filter(user=user).exists()


@transaction.atomic
@login_required(login_url='loge_ins')
@user_passes_test(cliente_check, login_url='welcome')
def comprarProducto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    compra = Compra()
    if request.method == "POST":
        form = comprasForm(request.POST)
        if form.is_valid():
            unidades = form.cleaned_data['unidades']
               
            if unidades <= producto.unidades:
                cliente = get_object_or_404(Cliente, user=request.user)
                producto.unidades -= unidades
                producto.save()
                compra = Compra()
                compra.producto= producto
                compra.user= cliente
                compra.unidades=unidades
                compra.importe= unidades*producto.precio
                compra.fecha= timezone.now()
                compra.save()
                cliente.saldo -=compra.importe
                cliente.save()
                messages.info(request, "Compra finalizada")
                return redirect('compraRealizada', pk=compra.pk)
    form = comprasForm()            
    return render(request, 'tienda/checkout.html', {'form': form, 'producto': producto})



@transaction.atomic
@login_required(login_url='loge_ins')
@user_passes_test(cliente_check, login_url='loge_ins')
def compraRealizada(request, pk):
    compra = Compra.objects.get(pk=pk)
    producto = compra.producto
    importe = compra.unidades * producto.precio
    return render(request, 'tienda/compraTerminada.html', {'producto': producto, 'compra': compra, 'importe': importe})


@login_required(login_url='loge_ins')
@staff_member_required
def producto_top(request):
    producto_top = Producto.objects.annotate(sum_unidades=Sum('compra__unidades'), sum_importes=Sum('compra__importe')).order_by('-sum_unidades')[:10]
    return render(request, 'tienda/productoTop.html', {'producto_top': producto_top})


@login_required(login_url='loge_ins')
@user_passes_test(cliente_check, login_url='welcome')
def historial_compras(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    compras = Compra.objects.all().filter(producto__compra__user_id=cliente).order_by('-fecha')[:10]
    return render(request, 'tienda/historialC.html', {'compras': compras})


@login_required(login_url='loge_ins')
@staff_member_required
def clientesTop(request):
    top_cliente = Cliente.objects.annotate(dinero_gastado=Sum('compra__importe')).order_by('-dinero_gastado')[:3]
    return render(request, 'tienda/clientesTop.html', {'top_clientes': top_cliente})