from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Cliente, Compra
from django.contrib.admin.views.decorators import staff_member_required
from .form import cambiarProducto, iniciar_sesion, fitroForm, comprasForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum




#Esto enlazara con la pagina de inicio
def welcome(request):
    return render(request,'tienda/index.html', {})


#--------------------------------------------------------------------------------------------------

# Iniciaremos sesión
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
                cliente = cliente_check(user)
                if cliente:
                    return_render = redirect(next_ruta)
                    login(request, user)
                    return return_render
                else:
                     return return_render
        else:
            return return_render
    else:
        return return_render


def cerrar_sesion_view(request):
    logout(request)
    return redirect('welcome')


#--------------------------------------------------------------------------------------------------


@login_required(login_url='loge_ins')  # Obligara a que para entrar el usuario deba estar logeado
@staff_member_required  # Obligara a que el usuario sea un miembro del suff o admin
# Pasara todos los productos que ya existen en producto
def productos(request):
    Productos = Producto.objects.all()  # Coge todos los objetos que hay en productos
    return render(request, 'tienda/producto.html', {'Productos': Productos})


@login_required(login_url='loge_ins')
@staff_member_required
# Permitira editar los productos ya existentes
def editarProducto(request, pk):
    producto = get_object_or_404(Producto,
                                 pk=pk)  # Recupera los objetos de la clase producto ,el pk=pk se utilizara para buscar el objeto Producto que tenga la clave primaria que coincida con el valor de pk.
    if request.method == "POST":
        form = cambiarProducto(request.POST,
                               instance=producto)  # Inicializaremos un formulario con datos ya creados, al trabajar con formularios para editar datos existentes, se utiliza el argumento instance, instance=producto asigna un objeto ya creado al formulario.
        if form.is_valid():
            producto = form.save(
                commit=False)  # Generará una instancia del modelo producto con los datos del formulario. Cuando se pasa el argumento commit=False, se le indica a Django que no guarde inmediatamente los datos en la base de datos, sino que simplemente cree una instancia del modelo
            producto.save()  # Guardaremos los cambios realizados en la base de datos
            return redirect('productos')  # Nos redigirá a los productos
    else:  # Si la solicitud no es de tipo POST,   se inicializa el formulario con el objeto producto como instancia del formulario. Esto asegura que el formulario muestre los datos actuales del producto para su edición.
        form = cambiarProducto(instance=producto)
    return render(request, 'tienda/editar.html', {'form': form})  # Se renderiza y se envia el formulario


@login_required(login_url='loge_ins')
@staff_member_required
# Eliminará los productos ya existentes
def eliminarProducto(request, pk):
    producto = Producto.objects.filter(pk=pk).delete()  # Busca un objeto en la base de datos de la clase Producto donde la clave primaria (pk) es igual al valor proporcionado(La función filter() se utiliza para filtrar los objetos en función de ciertos criterios, y en este caso, se filtra por la clave primaria), y luego lo borra de la base de datos
    return redirect('productos')


@login_required(login_url='loge_ins')
@staff_member_required
# Añadira un nuevo producto
def añadirProducto(request):
    if request.method == "POST":
        form = cambiarProducto(request.POST)  # Inicializaremos un formulario con los datos enviados por el usuario
        if form.is_valid():
            form.save()  # Guardaremos los datos introducidos en la base de datos
            return redirect('productos')
    else:  # Si la solicitud no es de tipo POST , inicializamos un formulario vacío para mostrar al usuario
        form = cambiarProducto()
    return render(request, 'tienda/nuevo.html', {'form': form})



#--------------------------------------------------------------------------------------------------


# Enlazara con la pagina tienda y mostrara una lista de los productos que ya existen
def tienda(request):
    productos = Producto.objects.all() #Recuperara los objetos de la calse productos de la base de datos de producto en models
    filtro_prod = fitroForm() #Cogeremos el filtro de form para poder buscar por nombre y marca

    if request.method == "POST": #Comprueba si la solicitud que está llegando al servidor es de tipo POST.
        filtro_prod = fitroForm(request.POST) #Se inicializa el formulario fitroForm con los datos enviados mediante request.POST.
        if filtro_prod.is_valid():  #Validaremos si los datos introducidos son correctos
            nombre = filtro_prod.cleaned_data['nombre'] #Cogeremos el nombre pasado
            marca = filtro_prod.cleaned_data['marca']

            productos = productos.filter(nombre__contains=nombre) #Filtraremos los productos por ese nombre, para solo mostrar los productos que contengan similitudes con el nombre
            if marca:
                productos = productos.filter(marca__id__in=marca)

    return render(request, 'tienda/tienda.html', {'Productos': productos, 'filtro_prod': filtro_prod}) #Pasaremos los datos, todos los datos que hay en producto y el filtro para buscar los nombres de cada producto


#Utilizaremos esto para verificar si el usuario es o no un cliente
def cliente_check(user):
    return Cliente.objects.filter(user=user).exists()


@transaction.atomic #Es un decorador que se utiliza para garantizar que un bloque de código se ejecute en una transacción de base de datos atómica.
def comprarProducto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = comprasForm(request.POST)
        if form.is_valid():
            unidades = form.cleaned_data['unidades']

            if unidades <= producto.unidades:
                cliente = Cliente.objects.get(user=request.user)
                producto.unidades -= unidades
                producto.save()
                compra = Compra()
                compra.producto = producto
                compra.user = cliente
                compra.unidades = unidades
                compra.importe = unidades * producto.precio
                compra.fecha = timezone.now()
                compra.save()
                cliente.saldo -= compra.importe
                cliente.save()
                messages.info(request, "Compra finalizada")
                return redirect('checkout', pk=compra.pk)
    form = comprasForm()
    return render(request, 'tienda/compraProducto.html', {'form': form, 'producto': producto})


#Nos mostrara el total gastado en la compra y los datos de ella
@login_required(login_url='loge_ins')
@user_passes_test(cliente_check, login_url='loge_ins')
def checkout(request, pk):
    compra = Compra.objects.get(pk=pk)
    producto = compra.producto
    importe = compra.unidades * producto.precio
    return render(request, 'tienda/checkout.html', {'producto': producto, 'compra': compra, 'importe': importe})



#--------------------------------------------------------------------------------------------------


#En info mostraremos todos los productos, podremos buscarlos y marcalos según su marca y nombre, es igual al anterior view de tienda

@login_required(login_url='loge_ins')
@staff_member_required
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

    return render(request,'tienda/info.html', {'Productos':productos,'filtro_prod':filtro_prod})



#Mostrara los productos más vendidos en la tienda
@login_required(login_url='loge_ins')
@staff_member_required
def producto_top(request):
    producto_top = Producto.objects.annotate(sum_unidades=Sum('compra__unidades'), sum_importes=Sum('compra__importe')).order_by('-sum_unidades')[:10] #annotate() se utiliza para realizar operaciones de agregación en los objetos
    return render(request, 'tienda/info.html', {'producto_top': producto_top})


@login_required(login_url='loge_ins')
@staff_member_required
def historial_compras(request):
    compras = Compra.objects.all().annotate(Count('fecha', distinct=True)).order_by('-fecha')[:10] 
    return render(request, 'tienda/info.html', {'compras': compras})


@login_required(login_url='loge_ins')
@staff_member_required
def clientesTop(request):
    top_cliente = Cliente.objects.annotate(dinero_gastado=Sum('compra__importe')).order_by('-dinero_gastado')[:3]
    return render(request, 'tienda/info.html', {'top_clientes': top_cliente})