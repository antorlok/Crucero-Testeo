from apps.almacen.signals import productosSignal

# Función receptora de la señal productosSignal
@productosSignal.connect
def productos_bajos_receiver(sender, **kwargs):
    productos = kwargs.get('productos')

    barco_id = kwargs.get('barco_id')
    if productos:
        from apps.compras.compras.models import SolicitudCompra, SolicitudCompraItem
        solicitud = SolicitudCompra.objects.create(barco_id=barco_id)
        for producto in productos:
            SolicitudCompraItem.objects.create(
                solicitud=solicitud,
                nombre=getattr(producto, 'nombre', ''),
                cantidad=getattr(producto, 'cantidad', 0),
                medida=getattr(producto, 'medida', '')
            )

