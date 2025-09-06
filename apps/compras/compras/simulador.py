from .models import SolicitudSubtipo, SolicitudSubtipoItem
from django.http import HttpResponse
import random

def crear_solicitudes_simuladas_util():
    # Crea 10 solicitudes grandes, cada una con 20-40 items
    for i in range(10):
        solicitud = SolicitudSubtipo.objects.create(
            tipo=random.choice(['COMIDA', 'BIENES']),
            subtipo=random.choice(['CADUCABLE', 'NO_CADUCABLE', 'REFRIGERADO', 'NO_REFRIGERADO', 'BEBIDA', 'LICOR', 'REPUESTOS', 'LIMPIEZA', 'MEDICOS', 'ACTIVOS'])
        )
        num_items = random.randint(20, 40)
        for j in range(num_items):
            SolicitudSubtipoItem.objects.create(
                solicitud=solicitud,
                producto_id=random.randint(1000, 9999),
                nombre=f"Producto {i}-{j}",
                cantidad_a_comprar=random.randint(1, 100),
                medida=random.choice(['kg', 'und', 'l']),
                tipo=solicitud.tipo,
                subtipo=solicitud.subtipo
            )
