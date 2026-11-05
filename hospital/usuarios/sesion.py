from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

from .models import Usuario

CLAVE_SESION = 'usuario_id'


def usuario_en_sesion(request):
    """Devuelve el Usuario que inició sesión, o None."""
    usuario_id = request.session.get(CLAVE_SESION)
    if usuario_id is None:
        return None
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if usuario is None:
        # El usuario fue eliminado después de iniciar sesión.
        request.session.flush()
    return usuario


def ir_al_login(request):
    return redirect(f"{reverse('login_usuario')}?{urlencode({'next': request.path})}")


def login_requerido(vista):
    """Solo deja pasar a usuarios registrados que iniciaron sesión."""
    @wraps(vista)
    def envoltura(request, *args, **kwargs):
        request.usuario_actual = usuario_en_sesion(request)
        if request.usuario_actual is None:
            return ir_al_login(request)
        return vista(request, *args, **kwargs)
    return envoltura
