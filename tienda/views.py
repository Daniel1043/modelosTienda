from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .form import cambiarProducto

# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def productos(request):
    Productos=Producto.objects.filter()
    return render(request, 'tienda/producto.html', {'Productos':Productos})


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


def eliminarProducto(request, pk):
    producto=Producto.objects.filter(pk=pk).delete()
    return redirect('productos')