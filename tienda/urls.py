from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.tienda, name='tienda'),
    path('tienda/admin/producto', views.productos, name='productos'),
    path('tienda/admin/editar/<int:pk>', views.editarProducto, name='editarProducto'),
    path('tienda/admin/eliminar/<int:pk>', views.eliminarProducto, name='eliminarProducto'),
    path('tienda/admin/nuevo/', views.añadirProducto, name='añadirProducto'),
    path('tienda/busqueda/', views.buscar, name='buscar'),
    path('tienda/iniciar/', views.loge_ins, name='loge_ins'),
]
