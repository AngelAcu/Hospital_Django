from django.http import HttpResponse
from django.shortcuts import render

from .models import HistoriaClinica, PacienteHistoria


def inicio(request):
    return HttpResponse("<h1>Hola mundo</h1> <br> <p>Hola mundo</p>")


def create(request):
    data = HistoriaClinica.objects.create(
        paciente=PacienteHistoria(
            documento="12345678",
            nombre="Ángel Acuña",
            fecha_nacimiento="1990-05-20",
            telefono="3001234567",
        ),
        antecedentes="Hipertensión",
        alergias="Penicilina",
        observaciones="Paciente estable",
    )
    return render(request, 'historias_clinicas/create.html', {'historia': data})


def find(request):        
    data = HistoriaClinica.objects.all()
    return render(request, 'historias_clinicas/find.html', {'historias': data})


def update(request):
    data = HistoriaClinica.objects.first()
    data.antecedentes = "Hipertensión, Diabetes"
    data.alergias = "Penicilina, Ibuprofeno"
    data.observaciones = "Paciente actualizado"
    data.save()
    return render(request, 'historias_clinicas/update.html', {'historia': data})


def delete(request):
    data = HistoriaClinica.objects.first()
    data.delete()
    return render(request, 'historias_clinicas/delete.html', {'historia': data})