from django.http import HttpResponse
from django.shortcuts import render

from .models import Medicamento

# Create your views here.
def inicio(request):
    return HttpResponse("<h1>Hola mundo</h1> <br> <p>Hola mundo</p>")

def create(request):
    data = Medicamento.objects.create(
        nombre="Acetaminofén",
        descripcion="Medicamento para aliviar el dolor y la fiebre",
        stock=100,
        precio=5000.0,
        fecha_vencimiento="2027-12-31",
        codigo="MED006"
    )
    
    return render(request, 'create.html', {'medicamento': data})

def find(request):
    data = Medicamento.objects.all()
    
    return render(request, 'find.html', {'medicamentos': data})

def delete(request):
    data = Medicamento.objects.get(codigo='MED006')
    data.delete()
    
    return render(request, 'delete.html', {'medicamento': data})

def update(request):
    data = Medicamento.objects.get(codigo='MED006')
    
    data.precio = 2500
    data.stock = 15
    data.nombre = "clonazepaam"
    data.descripcion = "medicamento actualizado"
    
    data.save()
    
    return render(request, 'update.html', {'medicamento': data})