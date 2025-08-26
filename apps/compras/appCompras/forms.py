    # /crucero copia/Administracion-proyecto-Crucero/apps/compras/appCompras/forms.py
from django import forms
from .models import SolicitudCompra, Proveedor # Importa los nuevos modelos

class SolicitudCompraForm(forms.ModelForm):
        class Meta:
            model = SolicitudCompra
            fields = '__all__' # O los campos específicos que quieras en el formulario

class ProveedorForm(forms.ModelForm):
        class Meta:
            model = Proveedor
            fields = '__all__'
    