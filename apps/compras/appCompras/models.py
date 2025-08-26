    # /crucero copia/Administracion-proyecto-Crucero/apps/compras/appCompras/models.py
from django.db import models
    # from myApp.models import Crucero # Si necesitas vincular solicitudes a cruceros específicos

class Proveedor(models.Model):
        nombre = models.CharField(max_length=255)
        contacto = models.CharField(max_length=255, blank=True, null=True)
        telefono = models.CharField(max_length=20, blank=True, null=True)
        email = models.EmailField(blank=True, null=True)
        # Otros campos relevantes para el proveedor

        def __str__(self):
            return self.nombre

class SolicitudCompra(models.Model):
        # crucero = models.ForeignKey(Crucero, on_delete=models.CASCADE, related_name='solicitudes_compra') # Si se vincula a un crucero
        fecha_solicitud = models.DateField(auto_now_add=True)
        descripcion_general = models.TextField(blank=True, null=True)
        estado = models.CharField(
            max_length=50,
            choices=[
                ('pendiente', 'Pendiente'),
                ('aprobada', 'Aprobada'),
                ('en_proceso', 'En Proceso'),
                ('completada', 'Completada'),
                ('cancelada', 'Cancelada'),
            ],
            default='pendiente'
        )
        # Podrías tener una relación ManyToMany con un modelo ItemSolicitado si cada solicitud tiene múltiples ítems
        # o simplemente campos para el total y el proveedor si la solicitud es para un único proveedor/compra grande.
        proveedor_sugerido = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
        total_estimado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

        def __str__(self):
            return f"Solicitud {self.id} - {self.estado}"

    # El modelo Compra existente podría usarse para registrar las compras una vez que se ejecutan las solicitudes.
    # class Compra(models.Model):
    #     ...
    
