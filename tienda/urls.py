from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/producto', views.productos, name='productos'),
    path('tienda/admin/editar/<int:pk>', views.editarProducto, name='editarProducto'),
    path('tienda/admin/eliminar/<int:pk>', views.eliminarProducto, name='eliminarProducto'),
]
