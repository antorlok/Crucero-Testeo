
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
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        materiales_json = request.POST.get('materiales_json', '[]')
        materiales_nombres = json.loads(materiales_json)
        paises_json = request.POST.get('paises_json', '[]')
        paises_nombres = json.loads(paises_json)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.save()
            materiales_objs = [Material.objects.get_or_create(nombre=nombre)[0] for nombre in materiales_nombres]
            proveedor.materiales.set(materiales_objs)
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