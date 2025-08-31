from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

# Solicitud de compra que agrupa varios artículos
class SolicitudCompra(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
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

class Paises(models.Model):
    nombre = models.CharField(max_length=100)

class Proveedores(models.Model):
    name = models.CharField(max_length=100)
    service_or_product = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    countries = models.ManyToManyField(Paises)
    sucursal = models.CharField(max_length=100)
    materiales = models.ManyToManyField(Material)

