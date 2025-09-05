from django.http import HttpResponseRedirect
from django.urls import reverse
# View para mostrar detalles de una solicitud
def detalle_solicitud_view(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCompra, id=solicitud_id)
    return render(request, 'detalle_solicitud.html', {'solicitud': solicitud})

# View para procesar una solicitud
def procesar_solicitud_view(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCompra, id=solicitud_id)
    if request.method == 'POST':
        solicitud.procesada = True
        solicitud.save()
        return HttpResponseRedirect(reverse('lista_solicitudes'))
    return HttpResponseRedirect(reverse('lista_solicitudes'))
# Vista para mostrar compras registradas

def compras_registradas_view(request):
    from .models import Compra
    if request.method == 'POST':
        compra_id = request.POST.get('compra_id')
        nuevo_estado = request.POST.get('nuevo_estado')
        if compra_id and nuevo_estado:
            try:
                compra = Compra.objects.get(id=compra_id)
                compra.estado = nuevo_estado
                compra.save()
            except Compra.DoesNotExist:
                pass
    compras = Compra.objects.exclude(estado__in=['exitosa', 'cancelada']).order_by('-fecha')
    return render(request, 'compras_registradas.html', {'compras': compras})
import json
from .models import Compra, CompraPorProveedor, ProveedorMaterial
# Vista para registrar una compra

def registrar_compra_view(request):
    from .models import Proveedores, Material
    proveedores = Proveedores.objects.all()
    # Construir diccionario de materiales por proveedor para JS
    proveedor_materiales = {}
    proveedor_paises = {}
    for proveedor in proveedores:
        mats = ProveedorMaterial.objects.filter(proveedor=proveedor)
        proveedor_materiales[proveedor.id] = [
            {'id': m.material.id, 'nombre': m.material.nombre, 'costo': float(m.costo_unidad)} for m in mats
        ]
        proveedor_paises[proveedor.id] = [
            {'id': pais.id, 'nombre': pais.nombre} for pais in proveedor.countries.all()
        ]
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        pais_id = request.POST.get('pais_entrega')
        sitio_llegada = request.POST.get('sitio_llegada')
        proveedor = Proveedores.objects.get(id=proveedor_id)
        pais = None
        if pais_id:
            from .models import Paises
            pais = Paises.objects.get(id=pais_id)
        # Crear la compra principal
        compra = Compra.objects.create(
            pais_entrega=pais,
            sitio_llegada=sitio_llegada
        )
        # Crear el registro de compra por proveedor
        descripcion = request.POST.get('descripcion', '')
        compra_proveedor = CompraPorProveedor.objects.create(
            compra=compra,
            proveedor=proveedor,
            descripcion=descripcion
        )
        # Procesar materiales dinámicos
        materiales_data = []
        for key in request.POST:
            if key.startswith('material_'):
                idx = key.split('_')[1]
                try:
                    material_id = request.POST.get(f'material_{idx}')
                    unidad = request.POST.get(f'unidad_{idx}')
                    cantidad = float(request.POST.get(f'cantidad_{idx}', '0'))
                    precio_unitario = float(request.POST.get(f'precio_unitario_{idx}', '0'))
                    total = cantidad * precio_unitario
                    materiales_data.append({
                        'material_id': material_id,
                        'unidad': unidad,
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario,
                        'total': total
                    })
                except Exception:
                    continue
        from .models import Material, CompraPorProveedorMaterial
        for mat in materiales_data:
            material = Material.objects.get(id=mat['material_id'])
            CompraPorProveedorMaterial.objects.create(
                compra_por_proveedor=compra_proveedor,
                material=material,
                unidad=mat['unidad'],
                cantidad=mat['cantidad'],
                precio_unitario=mat['precio_unitario'],
                total=mat['total']
            )
        return redirect('dashboard')
    return render(request, 'registrar_compra.html', {
        'proveedores': proveedores,
        'proveedor_materiales_json': json.dumps(proveedor_materiales),
        'proveedor_paises_json': json.dumps(proveedor_paises)
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Proveedores, Paises, Material
from .forms import ProveedorForm

from .models import SolicitudCompra, SolicitudCompraItem

# View para registrar solicitud de compra
@csrf_protect
def registrar_solicitud_compra_view(request):
    if request.method == 'POST':
        nombres = request.POST.getlist('nombre[]')
        cantidades = request.POST.getlist('cantidad[]')
        medidas = request.POST.getlist('medida[]')
        solicitud = SolicitudCompra.objects.create()
        for nombre, cantidad, medida in zip(nombres, cantidades, medidas):
            SolicitudCompraItem.objects.create(
                solicitud=solicitud,
                nombre=nombre,
                cantidad=cantidad,
                medida=medida
            )
        return redirect('lista_solicitudes')
    return render(request, 'solicitud_compra_form.html')

# View para listar solicitudes de compra
def lista_solicitudes_view(request):
    solicitudes = SolicitudCompra.objects.prefetch_related('items').order_by('-id')
    return render(request, 'lista_solicitudes.html', {'solicitudes': solicitudes})


@csrf_protect
def dashboard_view(request):
    return render(request, 'index.html')

@csrf_protect
def proveedores_view(request):
    import json
    from .models import ProveedorMaterial, Material, Paises
    SUBTIPOS_POR_TIPO = {
        'COMIDA': [
            ('CADUCABLE', 'Caducable'),
            ('NO_CADUCABLE', 'No caducable'),
            ('REFRIGERADO', 'Refrigerado'),
            ('NO_REFRIGERADO', 'No refrigerado'),
            ('BEBIDA', 'Bebida'),
            ('LICOR', 'Licor'),
        ],
        'BIENES': [
            ('REPUESTOS', 'Repuestos'),
            ('LIMPIEZA', 'Materiales de limpieza'),
            ('MEDICOS', 'Materiales médicos'),
            ('ACTIVOS', 'Bienes activos'),
        ]
    }
    tipo_seleccionado = None
    if request.method == 'POST':
        tipo_seleccionado = request.POST.get('tipo', None)
        form = ProveedorForm(request.POST)
        paises_json = request.POST.get('paises_json', '[]')
        if paises_json.strip() == '':
            paises_nombres = []
        else:
            paises_nombres = json.loads(paises_json)
        # Solo guardar si el submit fue por el botón Registrar
        if request.POST.get('action') == 'Registrar':
            if form.is_valid():
                proveedor = form.save(commit=False)
                proveedor.save()
                # Guardar países
                paises_objs = [Paises.objects.get_or_create(nombre=nombre)[0] for nombre in paises_nombres]
                proveedor.countries.set(paises_objs)
                return redirect('proveedores')
    else:
        form = ProveedorForm()
    proveedores = Proveedores.objects.all()
    return render(request, 'proveedores.html', {
        'form': form,
        'proveedores': proveedores,
        'SUBTIPOS_POR_TIPO': SUBTIPOS_POR_TIPO,
        'tipo_seleccionado': tipo_seleccionado,
    })

@csrf_protect
def eliminar_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor_id')
        if not proveedor_id:
            return redirect('proveedores')
        proveedor = get_object_or_404(Proveedores, id=proveedor_id)
    proveedor.countries.clear()
    proveedor.delete()
    return redirect('proveedores')
    return redirect('proveedores')
def historial_compras_view(request):
    from .models import Compra
    compras = Compra.objects.filter(estado__in=['exitosa', 'cancelada']).order_by('-fecha')
    return render(request, 'historial_compras.html', {'compras': compras})