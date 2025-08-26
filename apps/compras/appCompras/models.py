from django.db import models

class Compra(models.Model):
    descripcion = models.CharField(max_length=255)
    fecha = models.DateField()
    proveedor = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f"{self.descripcion} - {self.proveedor}"
