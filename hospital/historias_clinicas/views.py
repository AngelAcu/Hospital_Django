from django.shortcuts import render
from django.http import HttpResponse
from .models import HistoriaClinica, PacienteHistoria


def inicio(request):
    return HttpResponse( '<h1>Hola mundo</h1> <br> <p>Hola mundo</p>')

def create(request):
    data = {
        'id':1,
        'paciente':{
            'documento':'12334421312',
            'nombre':'Juan Perez',
            'fecha_nacimiento':'1990-09-12',
            'telefono':'3126409530',
        },
        'fecha_creacion': '2026-10-12 10:30:00 ',
        'antecedentes':'Hipertensión',
        'alergias':'Penicilina',
        'observaciones':'paciente estable',

    }
    return render( request,'historias_clinicas/create.html',{'historia':data})
def find(request):
    data = [
        {
            'id': 1,
            'paciente': {
                'documento': '12345678',
                'nombre': 'angel acuña',
                'fecha_nacimiento': '1990-05-20',
                'telefono': '3001234567',
            },
            'fecha_creacion': '2026-10-12 10:30:00',
            'antecedentes': 'Hipertensión',
            'alergias': 'Penicilina',
            'observaciones': 'Paciente estable',
        },
        {
            'id': 2,
            'paciente': {
                'documento': '87654321',
                'nombre': 'sebastian morales',
                'fecha_nacimiento': '1985-11-02',
                'telefono': '3109876543',
            },
            'fecha_creacion': '2026-10-12 11:00:00',
            'antecedentes': 'Asma',
            'alergias': 'Ninguna',
            'observaciones': 'Control mensual',
        },
        {
            'id': 3,
            'paciente': {
                'documento': '11223344',
                'nombre': 'Alejandra Gonzales',
                'fecha_nacimiento': '2000-03-10',
                'telefono': '3205556677',
            },
            'fecha_creacion': '2026-10-12 11:30:00',
            'antecedentes': 'Diabetes tipo 2',
            'alergias': 'Sulfas',
            'observaciones': 'Requiere seguimiento',
        },
    ]
    return render(request, 'historias_clinicas/find.html', {'historias': data})
def update(request):
    data = {
        'id': 1,
        'paciente': {
            'documento': '12345678',
            'nombre': 'Angel Acuña',
            'fecha_nacimiento': '1990-05-20',
            'telefono': '3009999999',
        },
        'fecha_creacion': '2026-10-12 10:30:00',
        'antecedentes': 'Hipertensión, Diabetes',
        'alergias': 'Penicilina, Ibuprofeno',
        'observaciones': 'Paciente actualizado',
    }

    return render(request, 'historias_clinicas/update.html', {'historia': data})
def delete(request):
    data = {
        'id': 3,
        'paciente': {
            'documento': '11223344',
            'nombre': 'Carlos Ruiz',
            'fecha_nacimiento': '2000-03-10',
            'telefono': '3205556677',
        },
        'fecha_creacion': '2026-10-12 11:30:00',
        'antecedentes': 'Diabetes tipo 2',
        'alergias': 'Sulfas',
        'observaciones': 'Requiere seguimiento',
    }

    return render(request, 'historias_clinicas/delete.html', {'historia': data})
# Create your views here.
