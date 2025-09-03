# Vista para mostrar compras registradas

def compras_registradas_view(request):
    from .models import Compra
    if request.method == 'POST':
        compra_id = request.POST.get('compra_id')
        nuevo_estado = request.POST.get('nuevo_estado')
        if compra_id and nuevo_estado:
            compra = Compra.objects.get(id=compra_id)
            compra.estado = nuevo_estado
            compra.save()
    compras = Compra.objects.all().order_by('-fecha')
    return render(request, 'compras_registradas.html', {'compras': compras})
import json
from .models import Compra, CompraPorProveedor, ProveedorMaterial
# Vista para registrar una compra

def registrar_compra_view(request):
    from .models import Proveedores, Material
    proveedores = Proveedores.objects.all()
    # Construir diccionario de materiales por proveedor para JS
    proveedor_materiales = {}
    for proveedor in proveedores:
        mats = ProveedorMaterial.objects.filter(proveedor=proveedor)
        proveedor_materiales[proveedor.id] = [
            {'id': m.material.id, 'nombre': m.material.nombre, 'costo': float(m.costo_unidad)} for m in mats
        ]
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        material_id = request.POST.get('material')
        descripcion = request.POST.get('descripcion')
        unidad = request.POST.get('unidad')
        cantidad = float(request.POST.get('cantidad', '0'))
        precio_unitario = float(request.POST.get('precio_unitario', '0'))
        total = cantidad * precio_unitario
        # Crear la compra y el detalle
        compra = Compra.objects.create()
        proveedor = Proveedores.objects.get(id=proveedor_id)
        material = Material.objects.get(id=material_id)
        CompraPorProveedor.objects.create(
            compra=compra,
            proveedor=proveedor,
            material=material,
            descripcion=descripcion,
            unidad=unidad,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            total=total
        )
        return redirect('dashboard')
    return render(request, 'registrar_compra.html', {
        'proveedores': proveedores,
        'proveedor_materiales_json': json.dumps(proveedor_materiales)
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import Proveedores, Paises, Material
from .forms import ProveedorForm


@csrf_protect
def dashboard_view(request):
    return render(request, 'index.html')

@csrf_protect
def proveedores_view(request):
    import json
    from .models import ProveedorMaterial, Material, Paises
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        materiales_json = request.POST.get('materiales_json', '[]')
        materiales_data = json.loads(materiales_json)  # lista de {nombre, costo}
        paises_json = request.POST.get('paises_json', '[]')
        paises_nombres = json.loads(paises_json)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.save()
            # Limpiar relaciones previas si es edición (opcional)
            proveedor.materiales.clear()
            # Guardar materiales y costos
            for mat in materiales_data:
                nombre = mat.get('nombre')
                costo = mat.get('costo')
                if nombre and costo is not None:
                    material_obj, _ = Material.objects.get_or_create(nombre=nombre)
                    ProveedorMaterial.objects.create(
                        proveedor=proveedor,
                        material=material_obj,
                        costo_unidad=costo
                    )
            # Guardar países
            paises_objs = [Paises.objects.get_or_create(nombre=nombre)[0] for nombre in paises_nombres]
            proveedor.countries.set(paises_objs)
            return redirect('proveedores')
    else:
        form = ProveedorForm()
    proveedores = Proveedores.objects.all()
    return render(request, 'proveedores.html', {'form': form, 'proveedores': proveedores})

@csrf_protect
def eliminar_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor_id')
        if not proveedor_id:
            return redirect('proveedores')
        proveedor = get_object_or_404(Proveedores, id=proveedor_id)
        proveedor.countries.clear()
        proveedor.materiales.clear()
        proveedor.delete()
        return redirect('proveedores')
    return redirect('proveedores')