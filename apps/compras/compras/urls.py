
from django.urls import path
from .views import dashboard_view, proveedores_view, eliminar_proveedor

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('proveedores/', proveedores_view, name='proveedores'),
    path('proveedores/eliminar/', eliminar_proveedor, name='eliminar_proveedor'),
]
