from django.dispatch import Signal

# from apps.almacen.signals import productosSignal
# from apps.compras.otros_signals import aceptado_signal

# Función receptora de la señal productosSignal

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
# productosSignal.connect(productos_bajos_receiver)


#  Función receptora de la señal aceptado_signal
def aceptado_receiver(sender, **kwargs):
    aceptado = kwargs.get('aceptado')
    mensaje = kwargs.get('mensaje')
    print(f"Receiver: aceptado={aceptado}, mensaje={mensaje}")
# aceptado_signal.connect(aceptado_receiver)

#  Senders

monto_mensaje_signal = Signal()

def enviar_monto_mensaje(monto, mensaje=None):
    """
    Envía un signal con un monto y un mensaje usando Django signals.
    """
    if mensaje is None:
        mensaje = "Solicitud de Compra"
    monto_mensaje_signal.send(sender=None, monto=monto, mensaje=mensaje)
