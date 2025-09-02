
from django.urls import path
from . import views

urlpatterns = [
    path('proveedores/', views.proveedores_view, name='proveedores'),
    path('proveedores/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),
]
