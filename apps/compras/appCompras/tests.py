from django.test import TestCase
from .models import Compra
from datetime import date

class CompraModelTest(TestCase):
    def test_creacion_compra(self):
        compra = Compra.objects.create(
            descripcion='Compra de alimentos',
            fecha=date.today(),
            proveedor='Proveedor X',
            cantidad=10,
            precio_unitario=100.00,
            total=1000.00
        )
        self.assertEqual(compra.descripcion, 'Compra de alimentos')
