
from django.urls import path
from .views import dashboard_view, proveedores_view, eliminar_proveedor, registrar_compra_view, compras_registradas_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('proveedores/', proveedores_view, name='proveedores'),
    path('proveedores/eliminar/', eliminar_proveedor, name='eliminar_proveedor'),
    path('compras/registrar/', registrar_compra_view, name='registrar_compra'),
    path('compras/registradas/', compras_registradas_view, name='compras_registradas'),
]
