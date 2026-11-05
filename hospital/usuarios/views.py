from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .models import ROLES, Usuario
from .sesion import CLAVE_SESION, ir_al_login, login_requerido, usuario_en_sesion

# Igual que el minLength de password en el esquema JSON (migración 0004).
MIN_PASSWORD = 6


def _llenar(usuario, datos):
    usuario.nombre = datos.get('nombre', '').strip()
    usuario.documento = datos.get('documento', '').strip()
    usuario.fecha_nacimiento = datos.get('fecha_nacimiento', '').strip() or None
    usuario.email = datos.get('email', '').strip()
    usuario.usuario = datos.get('usuario', '').strip()
    usuario.telefono = datos.get('telefono', '').strip()
    rol = datos.get('rol', '')
    usuario.rol = {'nombre': rol, 'descripcion': dict(ROLES).get(rol, '')}


def _validar_y_guardar(usuario, password, password_obligatoria):
    """Valida con las reglas del modelo, cifra la contraseña y guarda. Devuelve los errores por campo."""
    errores = {}
    if password or password_obligatoria:
        if len(password) < MIN_PASSWORD:
            errores['password'] = [f'La contraseña debe tener al menos {MIN_PASSWORD} caracteres.']
        else:
            usuario.password = make_password(password)

    try:
        # password se valida arriba: aquí ya es un hash o sigue vacía por un error ya reportado.
        usuario.full_clean(exclude=['password'])
    except ValidationError as e:
        errores.update(e.message_dict)
        # Las plantillas no aceptan claves con "_" al inicio, como '__all__'.
        if '__all__' in errores:
            errores['general'] = errores.pop('__all__')

    if not errores:
        try:
            usuario.save()
        except DatabaseError:
            # El esquema JSON de MongoDB rechazó el documento.
            errores['general'] = ['La base de datos rechazó el registro. Revisa los datos e inténtalo de nuevo.']
    return errores


def _formulario(request, usuario, errores, titulo):
    return render(request, 'usuarios/form.html', {
        'usuario': usuario,
        # El campo de fecha del navegador espera AAAA-MM-DD.
        'fecha_nacimiento': str(usuario.fecha_nacimiento or ''),
        'errores': errores,
        'roles': ROLES,
        'titulo': titulo,
    })


def iniciar_sesion(request):
    destino = request.POST.get('next') or request.GET.get('next') or ''
    error = None
    if request.method == 'POST':
        usuario = Usuario.objects.filter(usuario=request.POST.get('usuario', '').strip()).first()
        if usuario and check_password(request.POST.get('password', ''), usuario.password):
            request.session.cycle_key()
            request.session[CLAVE_SESION] = usuario.id
            if not url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
                destino = reverse('find_historia')
            return redirect(destino)
        error = 'Usuario o contraseña incorrectos.'
    return render(request, 'usuarios/login.html', {'error': error, 'next': destino})


def cerrar_sesion(request):
    if request.method == 'POST':
        request.session.flush()
    return redirect('login_usuario')


@login_requerido
def inicio(request):
    return redirect('find_usuario')


def create(request):
    request.usuario_actual = usuario_en_sesion(request)
    # Sin sesión solo se permite crear el primer usuario del sistema.
    if request.usuario_actual is None and Usuario.objects.count():
        return ir_al_login(request)

    usuario = Usuario()
    errores = {}
    if request.method == 'POST':
        _llenar(usuario, request.POST)
        errores = _validar_y_guardar(usuario, request.POST.get('password', ''), password_obligatoria=True)
        if not errores:
            return render(request, 'usuarios/create.html', {'usuario': usuario})
    return _formulario(request, usuario, errores, 'Nuevo usuario')


@login_requerido
def find(request):
    data = Usuario.objects.all()

    return render(request, 'usuarios/find.html', {'usuarios': data})


@login_requerido
def update(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    errores = {}
    if request.method == 'POST':
        _llenar(usuario, request.POST)
        # Contraseña vacía = conservar la actual.
        errores = _validar_y_guardar(usuario, request.POST.get('password', ''), password_obligatoria=False)
        if not errores:
            return render(request, 'usuarios/update.html', {'usuario': usuario})
    return _formulario(request, usuario, errores, 'Editar usuario')


@login_requerido
def delete(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        try:
            usuario.delete()
        except ProtectedError:
            return render(request, 'usuarios/delete.html', {
                'usuario': usuario,
                'confirmar': True,
                'error': 'No se puede eliminar: este usuario tiene una historia clínica. Elimina primero la historia.',
            })
        return render(request, 'usuarios/delete.html', {'usuario': usuario})
    return render(request, 'usuarios/delete.html', {'usuario': usuario, 'confirmar': True})
