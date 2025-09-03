# Modelo para compras registradas con campo de estado

from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

# Solicitud de compra que agrupa varios artículos
class SolicitudCompra(models.Model):
    procesada = models.BooleanField(default=False)

class SolicitudCompraItem(models.Model):
    solicitud = models.ForeignKey(SolicitudCompra, related_name='items', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    cantidad = models.IntegerField(validators=[MaxValueValidator(10000)])
    medida = models.CharField(max_length=20)

class Solicitud(models.Model):
    name = models.CharField(max_length=2000)
    amount = models.IntegerField(validators=[MaxValueValidator(10000)])
    unit_type = models.CharField(max_length=10)

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

# Relación intermedia para asociar proveedor, material y costo
class ProveedorMaterial(models.Model):
    proveedor = models.ForeignKey('Proveedores', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    costo_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together = ('proveedor', 'material')
    def __str__(self):
        return f"{self.proveedor.name} - {self.material.nombre} (${self.costo_unidad})"
class Paises(models.Model):
    nombre = models.CharField(max_length=100)

class Proveedores(models.Model):
    name = models.CharField(max_length=100)
    service_or_product = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    countries = models.ManyToManyField(Paises)
    sucursal = models.CharField(max_length=100)
    materiales = models.ManyToManyField(Material, through='ProveedorMaterial')



# Modelo para compras registradas con campo de estado y datos en otro modelo
class Compra(models.Model):
    ESTADO_CHOICES = [
        ('registrada', 'Registrada'),
        ('procesada', 'Procesada'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='registrada')

    def __str__(self):
        return f"Compra #{self.id} - {self.get_estado_display()}"

# Datos de la compra por proveedor

UNIDAD_CHOICES = [
    ('kg', 'Kg'),
    ('und', 'Unidad'),
    ('l', 'Litro'),
]

class CompraPorProveedor(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    proveedor = models.ForeignKey('Proveedores', on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    unidad = models.CharField(max_length=10, choices=UNIDAD_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.compra} - {self.proveedor.name} - {self.material.nombre}"