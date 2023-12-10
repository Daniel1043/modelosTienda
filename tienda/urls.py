from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.tienda, name='tienda'),
    path('tienda/admin/productos', views.productos, name='productos'),
    path('tienda/admin/editar/<int:pk>', views.editarProducto, name='editarProducto'),
    path('tienda/admin/eliminar/<int:pk>', views.eliminarProducto, name='eliminarProducto'),
    path('tienda/admin/nuevo/', views.añadirProducto, name='añadirProducto'),
    path('tienda/iniciar/', views.loge_ins, name='loge_ins'),
    path('tienda/cerrar/', views.cerrar_sesion_view, name='cerrar_sesion_view'),
    path('tienda/detallesCompra/<int:pk>', views.comprarProducto, name='comprarProducto'),
    path('tienda/info/checkout/<int:pk>', views.checkout, name='checkout'),
    path('tienda/info', views.info, name='info'),
    path('tienda/info/productoTop', views.producto_top, name='producto_top'),
    path('tienda/info/historial_compras', views.historial_compras, name='historial_compras'),
    path('tienda/info/clientesTop', views.clientesTop, name='clientesTop'),
]
