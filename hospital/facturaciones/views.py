from django.http import HttpResponse
from django.shortcuts import render

from .models import Factura, ConceptoFactura, DatosPacienteFactura


def inicio(request):
    return HttpResponse("<h1>Hola mundo</h1> <br> <p>Hola mundo</p>")


def create(request):
    data = Factura.objects.create(
        total=130000.0,
        estado="Pendiente",
        observaciones="Factura generada por consulta",
        codigo="FAC-001",
        paciente=DatosPacienteFactura(
            documento="12345678",
            nombre="Juan Pérez",
        ),
    )
    data.conceptos = [
        ConceptoFactura(descripcion="Consulta médica general", valor=50000.0),
        ConceptoFactura(descripcion="Examen de laboratorio", valor=80000.0),
    ]
    data.save()

    return render(request, 'facturaciones/create.html', {'factura': data})


def find(request):
    data = Factura.objects.all()
    return render(request, 'facturaciones/find.html', {'facturas': data})


def update(request):
    data = Factura.objects.get(codigo="FAC-001")
    data.total = 175000.0
    data.estado = "Pagada"
    data.observaciones = "Factura actualizada"
    data.conceptos = [
        ConceptoFactura(descripcion="Consulta especializada", valor=75000.0),
        ConceptoFactura(descripcion="Examen de laboratorio", valor=100000.0),
    ]
    data.save()
    return render(request, 'facturaciones/update.html', {'factura': data})


def delete(request):
    data = Factura.objects.get(codigo="FAC-001")
    data.delete()
    return render(request, 'facturaciones/delete.html', {'factura': data})