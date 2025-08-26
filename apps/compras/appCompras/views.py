from django.shortcuts import render
from .models import Compra

def lista_compras(request):
    compras = Compra.objects.all()
    return render(request, 'compras/lista_compras.html', {'compras': compras})
