from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Proveedores
from .forms import ProveedorForm

def holamundo(request):
    from .models import Proveedores
    proveedores = Proveedores.objects.all()
    return render(request, 'index.html', {'proveedores': proveedores})

def proveedores_view(request):
    from .models import Material
    import json
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        materiales_json = request.POST.get('materiales_json', '[]')
        materiales_nombres = json.loads(materiales_json)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.save()
            materiales_objs = []
            for nombre in materiales_nombres:
                mat, created = Material.objects.get_or_create(nombre=nombre)
                materiales_objs.append(mat)
            proveedor.materiales.set(materiales_objs)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                proveedores = Proveedores.objects.all()
                proveedores_data = [
                    {
                        'name': p.name,
                        'service_or_product': p.service_or_product,
                        'categorie': p.categorie,
                        'contact': p.contact,
                        'countries': p.countries,
                        'sucursal': p.sucursal,
                        'materiales': [m.nombre for m in p.materiales.all()]
                    }
                    for p in proveedores
                ]
                return JsonResponse({'success': True, 'proveedores': proveedores_data})
            return redirect('proveedores')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False})
    else:
        form = ProveedorForm()
    proveedores = Proveedores.objects.all()
    return render(request, 'proveedores.html', {'form': form, 'proveedores': proveedores})