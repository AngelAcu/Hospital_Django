from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_datetime
from bson import ObjectId
from usuarios.models import Usuario

from usuarios.sesion import login_requerido

from .models import Cita


@login_requerido
def inicio(request):
    return redirect('find_cita')


def _datos_cita(request):
    errores = {}
    fecha = parse_datetime(request.POST.get('fecha', ''))
    if fecha is None:
        errores['fecha'] = 'Ingresa una fecha y hora válidas.'

    motivo = request.POST.get('motivo', '').strip()
    estado = request.POST.get('estado', 'Pendiente').strip()
    paciente = {
        'documento': request.POST.get('paciente_documento', '').strip(),
        'nombre': request.POST.get('paciente_nombre', '').strip(),
        'telefono': request.POST.get('paciente_telefono', '').strip(),
        'correo': request.POST.get('paciente_correo', '').strip(),
    }
    medico = {
        'documento': request.POST.get('medico_documento', '').strip(),
        'nombre': request.POST.get('medico_nombre', '').strip(),
        'especialidad': request.POST.get('medico_especialidad', '').strip(),
    }

    if not motivo:
        errores['motivo'] = 'El motivo de la cita es obligatorio.'
    if estado not in ('Pendiente', 'Confirmada', 'Cancelada'):
        errores['estado'] = 'Selecciona un estado válido.'
    for campo, etiqueta in (
        ('nombre', 'nombre del paciente'),
        ('documento', 'documento del paciente'),
    ):
        if not paciente[campo]:
            errores[f'paciente_{campo}'] = f'El {etiqueta} es obligatorio.'
    for campo, etiqueta in (
        ('nombre', 'nombre del médico'),
        ('especialidad', 'especialidad'),
    ):
        if not medico[campo]:
            errores[f'medico_{campo}'] = f'La {etiqueta} es obligatoria.'

    return fecha, motivo, estado, paciente, medico, errores


def _formulario_contexto(cita=None, errores=None, titulo='Nueva cita médica'):
    return {
        'cita': cita,
        'errores': errores or {},
        'estados': ('Pendiente', 'Confirmada', 'Cancelada'),
        'titulo': titulo,
        'pacientes': _usuarios_por_rol('Paciente'),
        'personal': _usuarios_por_roles(('Medico', 'Enfermero', 'Farmaceuta')),
    }


def _usuarios_por_rol(rol):
    """Filtra usuarios por un nombre almacenado dentro del rol embebido."""
    return [
        usuario for usuario in Usuario.objects.all()
        if usuario.rol and usuario.rol['nombre'] == rol
    ]


def _usuarios_por_roles(roles):
    """Filtra usuarios cuyos roles pertenecen al personal de salud."""
    return [
        usuario for usuario in Usuario.objects.all()
        if usuario.rol and usuario.rol['nombre'] in roles
    ]


@login_requerido
def create(request):
    cita_vacia = {
        'fecha': None,
        'motivo': '',
        'estado': 'Pendiente',
        'paciente': {
            'documento': '',
            'nombre': '',
            'telefono': '',
            'correo': ''
        },
        'medico': {
            'documento': '',
            'nombre': '',
            'especialidad': ''
        }
    }

    if request.method == 'POST':
        fecha, motivo, estado, paciente, medico, errores = _datos_cita(request)
        if not errores:
            data = Cita(
                fecha=fecha,
                motivo=motivo,
                estado=estado,
                paciente=paciente,
                medico=medico,
            )
            try:
                data.full_clean()
                data.save()
            except ValidationError as error:
                errores['general'] = error.messages
            else:
                return render(request, 'citas/create.html', {'cita': data})

        contexto_errores = _formulario_contexto(errores=errores)
        contexto_errores['cita'] = cita_vacia
        return render(request, 'citas/form.html', contexto_errores)

    contexto = _formulario_contexto(titulo='Nueva cita médica')
    contexto['cita'] = cita_vacia

    return render(request, 'citas/form.html', contexto)



@login_requerido
def find(request):
    data = Cita.objects.all()

    return render(
        request,
        'citas/find.html', {'citas': data}
    )


@login_requerido
def update(request, id):
    data = get_object_or_404(Cita, _id=ObjectId(id))
    if request.method == 'POST':
        fecha, motivo, estado, paciente, medico, errores = _datos_cita(request)
        if not errores:
            data.fecha = fecha
            data.motivo = motivo
            data.estado = estado
            data.paciente = paciente
            data.medico = medico
            try:
                data.full_clean()
                data.save()
            except ValidationError as error:
                errores['general'] = error.messages
            else:
                return render(request, 'citas/update.html', {'cita': data})
        return render(request, 'citas/form.html', _formulario_contexto(data, errores, 'Editar cita médica'))

    return render(request, 'citas/form.html', _formulario_contexto(data, titulo='Editar cita médica'))


@login_requerido
def delete(request, id):
    data = get_object_or_404(Cita, _id=ObjectId(id))
    if request.method == 'POST':
        data.estado = 'Cancelada'
        data.save()
        return render(request, 'citas/delete.html', {'cita': data})
    return render(request, 'citas/delete.html', {'cita': data, 'confirmar': True})