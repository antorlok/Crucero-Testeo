from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Solicitud(models.Model):
    name = models.CharField(max_length=2000)
    amount = models.IntegerField(validators=[MaxValueValidator(10000)])
    unit_type = models.CharField(max_length=10)

class Material(models.Model):
    nombre = models.CharField(max_length=100)

class Proveedores(models.Model):
    name = models.CharField(max_length=100)
    service_or_product = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    countries = models.CharField(max_length=1000)
    sucursal = models.CharField(max_length=100)
    materiales = models.ManyToManyField(Material)

