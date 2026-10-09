from django.http import HttpResponse
from django.shortcuts import render

from .models import Medicamento

# Create your views here.
def inicio(request):
    return HttpResponse("<h1>Hola mundo</h1> <br> <p>Hola mundo</p>")

def goIndex(request):
    data = Medicamento.objects.create(
        nombre="Acetaminofén",
        descripcion="Medicamento para aliviar el dolor y la fiebre",
        stock=100,
        precio=5000.0,
        fecha_vencimiento="2027-12-31",
        codigo="MED006"
    )
    
    ## data = { 'usuario': { 'id': 1, 'nombre': 'Angel' } }
    return render(request, 'index.html', {'medicamento': data})