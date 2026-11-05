from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Medicamento, Dispensacion
from .forms import FormularioFarmacias

def inicio(request):
    return HttpResponse("<h1>Hola mundo</h1> <br> <p>Hola mundo</p>")

def goParams(request, id):
    return HttpResponse(f"<h1>El id ingresado es {id}</h1>")

def goIndex(request, decision):
    data = {
        "id": "1",
        "nombre": "Juan",
        "esAdministrador": decision
    }
    
    data_ciclos = [
        {
            "id": "1020",
            "nombre": "naproxeno",
            "costo": 45000
        }, 
        {
            "id": "1060",
            "nombre": "amoxicilina",
            "costo": 95000
        },
        {
            "id": "1905",
            "nombre": "advil",
            "costo": 8700
        }
    ]
    
    return render(request, 'index.html', {"usuario": data, "medicamentos": data_ciclos})

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

def createDispensacion(request):
    data = Dispensacion.objects.create(
        cantidad=2,
        observacion="Dispensación de prueba",

        paciente={
            "documento": "123456789010",
            "nombre": "Angel David Acuña Meza"
        },

        medicamento={
            "codigo": "MED004",
            "nombre": "Acetaminofén",
            "precio": 5000.0
        }
    )

    return render(request, 'createDispensacion.html', {'dispensacion': data})


def findDispensacion(request):
    data = Dispensacion.objects.all()

    return render(request, 'findDispensacion.html', {'dispensaciones': data})

def deleteDispensacion(request):
    data = Dispensacion.objects.get(id=1)
    data.delete()

    return render(request, 'deleteDispensacion.html', {'dispensacion': data})

def updateDispensacion(request):
    data = Dispensacion.objects.get(id=3)

    data.cantidad = 5
    data.observacion = "Dispensación actualizada"
    
    data.paciente = {
        "documento": "1234567890",
        "nombre": "Angel David Acuña Meza"
    }

    data.medicamento = {
        "codigo": "MED006",
        "nombre": "Acetaminofén actualizado",
        "precio": 2500.0
    }

    data.save()

    return render(request, 'updateDispensacion.html', {'dispensacion': data})

def createFarmacia(request):
    if request.method == 'GET':
        if 'nombre' in request.GET:
            nombre = request.GET['nombre']
            
        return render(request, 'crear-farmacia.html', {'formulario': FormularioFarmacias})
    
    else:
        if 'nombre' in request.POST:
            nombre = request.POST['nombre']
            print(f"Se esta guardando el usuario {nombre}")
    
        ##return redirect('inicio')