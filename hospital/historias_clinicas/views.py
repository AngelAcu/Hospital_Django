from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, redirect, render

from usuarios.models import Usuario
from usuarios.sesion import login_requerido

from .models import HistoriaClinica

CAMPOS_CLINICOS = ('antecedentes', 'alergias', 'observaciones')


def _llenar(historia, datos):
    for campo in CAMPOS_CLINICOS:
        setattr(historia, campo, datos.get(campo, '').strip())


def _pacientes_disponibles():
    """Usuarios con rol Paciente que todavía no tienen historia clínica."""
    con_historia = {h.paciente_id for h in HistoriaClinica.objects.all()}
    # shortcut: filtra en Python; si hay miles de usuarios, filtrar el rol en la consulta a MongoDB.
    return [u for u in Usuario.objects.all() if u.es_paciente() and u.id not in con_historia]


def _validar_y_guardar(historia):
    """Valida la historia (paciente registrado, con rol Paciente y sin otra historia) y guarda."""
    errores = {}
    try:
        historia.full_clean()
    except ValidationError as e:
        errores.update(e.message_dict)
        # Las plantillas no aceptan claves con "_" al inicio, como '__all__'.
        if '__all__' in errores:
            errores['general'] = errores.pop('__all__')

    if not errores:
        try:
            historia.save()
        except DatabaseError:
            # El esquema JSON o el índice único de MongoDB rechazó el documento.
            errores['general'] = ['La base de datos rechazó el registro. Revisa los datos e inténtalo de nuevo.']
    return errores


def _formulario(request, historia, errores, titulo):
    return render(request, 'historias_clinicas/form.html', {
        'historia': historia,
        'pacientes': [] if historia.id else _pacientes_disponibles(),
        'errores': errores,
        'titulo': titulo,
    })


@login_requerido
def inicio(request):
    return redirect('find_historia')


@login_requerido
def create(request):
    historia = HistoriaClinica()
    errores = {}
    if request.method == 'POST':
        paciente = request.POST.get('paciente', '')
        historia.paciente_id = int(paciente) if paciente.isdigit() else None
        _llenar(historia, request.POST)
        errores = _validar_y_guardar(historia)
        if not errores:
            return render(request, 'historias_clinicas/create.html', {'historia': historia})
    return _formulario(request, historia, errores, 'Nueva historia clínica')


@login_requerido
def find(request):
    data = HistoriaClinica.objects.all()
    return render(request, 'historias_clinicas/find.html', {'historias': data})


@login_requerido
def update(request, id):
    historia = get_object_or_404(HistoriaClinica, id=id)
    errores = {}
    if request.method == 'POST':
        # El paciente no se cambia al editar: solo la información clínica.
        _llenar(historia, request.POST)
        errores = _validar_y_guardar(historia)
        if not errores:
            return render(request, 'historias_clinicas/update.html', {'historia': historia})
    return _formulario(request, historia, errores, 'Editar historia clínica')


@login_requerido
def delete(request, id):
    historia = get_object_or_404(HistoriaClinica, id=id)
    if request.method == 'POST':
        historia.delete()
        return render(request, 'historias_clinicas/delete.html', {'historia': historia})
    return render(request, 'historias_clinicas/delete.html', {'historia': historia, 'confirmar': True})
