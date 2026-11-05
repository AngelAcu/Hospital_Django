from django.shortcuts import render
from django.http import HttpResponse
from .models import Cita


# Create your views here.
def inicio(request):
    return HttpResponse(
        "<h1>Modulo de Citas</h1>"
        "<br>"
        "<p>Gestion de citas medicas del hospital</p>"
    )


def create(request):
    data = Cita.objects.create(
        fecha="2026-11-15T09:30:00",
        motivo="Consulta general",
        estado="Pendiente",
        paciente={
            "documento": "1001234567",
            "nombre": "Juan Perez",
            "telefono": "3001234567",
            "correo": "juan@gmail.com"
        },
        medico={
            "documento": "987654321",
            "nombre": "Maria Rodriguez",
            "especialidad": "Medicina general"
        }
    )

    return render(request, 'create.html', {'cita': data})


def find(request):
    data = Cita.objects.all()

    return render(
        request,
        'find.html',
        {'citas': data}
    )


def delete(request):
    data = Cita.objects.get(
        paciente__documento="1001234567",
        estado__in=["Pendiente", "Confirmada"]
    )

    data.estado = "Cancelada"
    data.save()

    return render(
        request,
        'delete.html',
        {'cita': data}
    )


def update(request):
    data = Cita.objects.get(
        paciente__documento="1001234567",
        estado__in=["Pendiente", "Confirmada"]
    )

    data.fecha = "2026-11-20T10:00:00"
    data.motivo = "Control medico general"
    data.estado = "Confirmada"

    data.save()

    return render(
        request,
        'update.html',
        {'cita': data}
    )