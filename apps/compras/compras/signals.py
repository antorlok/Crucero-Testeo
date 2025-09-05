from django.dispatch import Signal
from django.dispatch import receiver


### REVISAR, no se usa
# from apps.compras.otros_signals import aceptado_signal

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

###  ALMACEN

# Importacion para poder tener los tipos y subtipos
from apps.almacen.models import Producto
from apps.almacen.signals import falta_stock_signal
from .models import SolicitudSubtipo, SolicitudSubtipoItem

@receiver(falta_stock_signal)
def manejar_productos_signal(sender, productos, **kwargs):

	query_set_base_productos = productos

	if not query_set_base_productos.exists():
		return

	# Si el queryset contiene exactamente un solo producto, se puede procesar directo y terminar.
	if query_set_base_productos.count() == 1:
		# Placeholder: generar orden de compra para el único producto
		# generar_orden_compra(query_set_base_productos)
		return

	# Iterar por tipos definidos en el modelo
	for nombre_del_tipo, _ in Producto.TIPOS_PRODUCTO:
		query_set_de_productos_por_tipo = query_set_base_productos.filter(tipo=nombre_del_tipo)
		if not query_set_de_productos_por_tipo.exists():
			continue
		# Aca tendrían una función van a generar orden solo por tipo
		# generar_orden_compra(query_set_de_productos_por_tipo)

		# Subtipos válidos para este tipo (Si existen)
		subtipos_validos = Producto.SUBTIPOS_POR_TIPO.get(nombre_del_tipo, [])
		for subtipo_code in subtipos_validos:
			query_set_del_subtipo = query_set_de_productos_por_tipo.filter(subtipo=subtipo_code)
			if not query_set_del_subtipo.exists():
				continue
			# Generar la solicitud para este subtipo
			primer_producto = query_set_del_subtipo.first()
			tipo = primer_producto.tipo
			subtipo = primer_producto.subtipo
			solicitud = SolicitudSubtipo.objects.create(tipo=tipo, subtipo=subtipo)
			for producto in query_set_del_subtipo:
				cantidad_a_comprar = getattr(producto, 'cantidad_ideal', 0) - getattr(producto, 'cantidad', 0)
				SolicitudSubtipoItem.objects.create(
                    solicitud=solicitud,
                    producto_id=producto.id,
                    nombre=producto.nombre,
                    cantidad_a_comprar=cantidad_a_comprar,
                    medida=producto.medida,
                    tipo=tipo,
                    subtipo=subtipo
                )

    # Atributos que les puede interesar
    # producto.id
    # producto.nombre
    # producto.tipo
    # producto.subtipo
    # producto.cantidad (No es un atributo, se calcula según la cantidad que tiene cada lote registrado de ese producto)
    # producto.cantidad_ideal
    # producto.medida