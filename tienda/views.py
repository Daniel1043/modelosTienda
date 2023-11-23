from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .form import cambiarProducto, iniciar_sesion
from django.contrib.auth import authenticate, login



#Esto enlazara con la pagina de inicio
def welcome(request):
    return render(request,'tienda/index.html', {})

#Enlazara con la pagina tienda y mostrara una lista de los productos que ya existen
def tienda(request):
    Productos=Producto.objects.filter()
    return render(request, 'tienda/tienda.html', {'Productos':Productos})


#Similar al anterior, mostrara todos los productos que ya existen
def productos(request):
    if request.user.is_authenticated:
        Productos=Producto.objects.filter()
        return render(request, 'tienda/producto.html', {'Productos':Productos})
    else:
        return redirect('loge_ins')

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


#Te permitira eliminar los productos ya existentes
def eliminarProducto(request, pk):
    producto=Producto.objects.filter(pk=pk).delete()
    return redirect('productos')

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
    marca = Producto.objects.filter(marca=buscar)
    return render(request, 'tienda/busqueda.html', {'nombre': nombre, 'marca': marca, 'buscar':buscar})


#Iniciaremos sesion
def loge_ins(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    else:
        if request.method == "POST":
            form = iniciar_sesion(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('welcome')
                else:
                    form.add_error(None, 'Usuario no existe')
                    messages.error(request, "no es")
        else:
            form = iniciar_sesion()
        return render(request, 'tienda/iniciarSesion.html', {'form': form})


