    # /crucero copia/Administracion-proyecto-Crucero/apps/compras/appCompras/urls.py
from django.urls import path
from . import views

urlpatterns = [
        path('', views.lista_compras, name='lista_compras'), # Mantener esta para la página principal del módulo
        path('solicitudes/', views.solicitudes_compra, name='solicitudes_compra'),
        path('solicitudes/nueva/', views.crear_solicitud_compra, name='crear_solicitud_compra'),
        path('proveedores/', views.gestion_proveedores, name='gestion_proveedores'),
        path('proveedores/nuevo/', views.crear_proveedor, name='crear_proveedor'),
        # ... otras URLs para editar/eliminar solicitudes o proveedores
    ]
