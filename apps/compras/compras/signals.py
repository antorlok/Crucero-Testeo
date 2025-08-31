from apps.almacen.signals import productosSignal

# Función receptora de la señal productosSignal
@productosSignal.connect
def productos_bajos_receiver(sender, **kwargs):
    productos = kwargs.get('productos')

    if productos:
        from apps.compras.compras.models import SolicitudCompra, SolicitudCompraItem
        solicitud = SolicitudCompra.objects.create()
        for producto in productos:
            SolicitudCompraItem.objects.create(
                solicitud=solicitud,
                nombre=getattr(producto, 'nombre', ''),
                cantidad=getattr(producto, 'cantidad', 0),
                medida=getattr(producto, 'medida', '')
            )

