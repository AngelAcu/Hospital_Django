from django.http import HttpResponse
from django.shortcuts import render

from .models import Usuario


def inicio(request):
    return HttpResponse("<h1>Usuarios</h1> <br> <p>Gestión de usuarios del hospital</p>")


def create(request):
    data = Usuario.objects.create(
        nombre="Angel David Acuña Meza",
        email="angel@example.com",
        usuario="angel01",
        password="123456",
        telefono="3001234567",

        rol={
            "nombre": "Paciente",
            "descripcion": "Paciente del hospital"
        }
    )

    return render(request, 'usuarios/create.html', {'usuario': data})


def find(request):
    data = Usuario.objects.all()

    return render(request, 'usuarios/find.html', {'usuarios': data})


def delete(request):
    data = Usuario.objects.get(usuario='angel01')
    data.delete()

    return render(request, 'usuarios/delete.html', {'usuario': data})


def update(request):
    data = Usuario.objects.get(usuario='angel01')

    data.nombre = "Angel David actualizado"
    data.email = "angelactualizado@example.com"
    data.telefono = "3109876543"

    data.rol = {
        "nombre": "Administrador",
        "descripcion": "Administrador del hospital"
    }

    data.save()

    return render(request, 'usuarios/update.html', {'usuario': data})