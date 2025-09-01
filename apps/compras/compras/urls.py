from django.urls import path
from . import views

urlpatterns = [
    path('proveedores/', views.proveedores_view, name='proveedores'),
    path('proveedores/delete/<int:proveedor_id>/', views.delete_proveedor, name='delete_proveedor'),
]
