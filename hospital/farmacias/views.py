
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
from bson import ObjectId

from usuarios.sesion import login_requerido

from .models import Medicamento, Dispensacion
from usuarios.models import Usuario


@login_requerido
def inicio_medicamento(request):
    return redirect('find_medicamento')

def _datos_medicamento(request):
    errores = {}

    nombre = request.POST.get('nombre', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()
    codigo = request.POST.get('codigo', '').strip()
    fecha_vencimiento = parse_date(request.POST.get('fecha_vencimiento', ''))

    stock = request.POST.get('stock', '').strip()
    precio = request.POST.get('precio', '').strip()

    if not nombre:
        errores['nombre'] = ['El nombre del medicamento es obligatorio.']

    if not descripcion:
        errores['descripcion'] = ['La descripción es obligatoria.']

    if not codigo:
        errores['codigo'] = ['El código del medicamento es obligatorio.']

    if fecha_vencimiento is None:
        errores['fecha_vencimiento'] = [
            'Ingresa una fecha de vencimiento válida.'
        ]

    try:
        stock = int(stock)
        if stock <= 0:
            errores['stock'] = ['El stock no puede ser negativo o igual a 0.']
    except (ValueError, TypeError):
        stock = None
        errores['stock'] = ['Ingresa una cantidad de stock válida.']

    try:
        precio = float(precio)
        if precio < 0:
            errores['precio'] = ['El precio no puede ser negativo.']
        elif precio == 0:
            errores['precio'] = ['El precio debe ser mayor a 0']
    except (ValueError, TypeError):
        precio = None
        errores['precio'] = ['Ingresa un precio válido.']

    return {
        'nombre': nombre,
        'descripcion': descripcion,
        'codigo': codigo,
        'fecha_vencimiento': fecha_vencimiento,
        'stock': stock,
        'precio': precio,
    }, errores


def _formulario_contexto(medicamento=None, errores=None, titulo='Nuevo medicamento'):
    return {
        'medicamento': medicamento,
        'errores': errores or {},
        'titulo': titulo,
    }


@login_requerido
def create_medicamento(request):

    medicamento_vacio = {
        'nombre': '',
        'descripcion': '',
        'codigo': '',
        'fecha_vencimiento': None,
        'stock': 0,
        'precio': '',
    }

    if request.method == 'POST':

        datos, errores = _datos_medicamento(request)

        if not errores:
            data = Medicamento(**datos)

            try:
                data.full_clean()
                data.save()

            except ValidationError as error:
                errores['general'] = error.messages

            else:
                return render(
                    request,
                    'medicamentos/createMedicamento.html',
                    {'medicamento': data}
                )

        contexto = _formulario_contexto(errores=errores)
        contexto['medicamento'] = medicamento_vacio

        return render(
            request,
            'medicamentos/formMedicamento.html',
            contexto
        )

    contexto = _formulario_contexto()
    contexto['medicamento'] = medicamento_vacio

    return render(
        request,
        'medicamentos/formMedicamento.html',
        contexto
    )


@login_requerido
def find_medicamento(request):

    data = Medicamento.objects.all()

    return render(
        request,
        'medicamentos/findMedicamento.html',
        {'medicamentos': data}
    )


@login_requerido
def update_medicamento(request, id):

    data = get_object_or_404(
        Medicamento,
        _id=ObjectId(id)
    )

    if request.method == 'POST':

        datos, errores = _datos_medicamento(request)

        if not errores:
            data.nombre = datos['nombre']
            data.descripcion = datos['descripcion']
            data.codigo = datos['codigo']
            data.fecha_vencimiento = datos['fecha_vencimiento']
            data.stock = datos['stock']
            data.precio = datos['precio']

            try:
                data.full_clean()
                data.save()

            except ValidationError as error:
                errores['general'] = error.messages

            else:
                return render(
                    request,
                    'medicamentos/updateMedicamento.html',
                    {'medicamento': data}
                )

        return render(
            request,
            'medicamentos/formMedicamento.html',
            _formulario_contexto(
                data,
                errores,
                'Editar medicamento'
            )
        )

    return render(request, 'medicamentos/formMedicamento.html', _formulario_contexto(data, titulo='Editar medicamento'))

@login_requerido
def delete_medicamento(request, id):

    data = get_object_or_404(Medicamento, _id=ObjectId(id))

    if request.method == 'POST':

        data.delete()

        return render(request, 'medicamentos/deleteMedicamento.html', {'medicamento': data,'confirmar': False})

    return render(request,'medicamentos/deleteMedicamento.html',{'medicamento': data, 'confirmar': True})

## DISPENSACIONES

def _usuarios_dispensacion_por_rol(roles):
    return [
        usuario for usuario in Usuario.objects.all()
        if usuario.rol and usuario.rol['nombre'] in roles
    ]


def _formulario_contexto_dispensacion(
    dispensacion=None,
    errores=None,
    titulo='Nueva dispensación'
):
    return {
        'dispensacion': dispensacion,
        'errores': errores or {},
        'titulo': titulo,
        'pacientes': _usuarios_dispensacion_por_rol(('Paciente',)),
        'personal': _usuarios_dispensacion_por_rol(
            ('Medico', 'Enfermero', 'Farmaceuta')
        ),
        'medicamentos': Medicamento.objects.all(),
    }


def _datos_dispensacion(request):
    errores = {}

    paciente_documento = request.POST.get(
        'paciente_documento', ''
    ).strip()

    medico_documento = request.POST.get(
        'medico_documento', ''
    ).strip()

    medicamento_codigo = request.POST.get(
        'medicamento_codigo', ''
    ).strip()

    observacion = request.POST.get(
        'observacion', ''
    ).strip()

    cantidad = request.POST.get('cantidad', '').strip()

    try:
        cantidad = int(cantidad)

        if cantidad <= 0:
            errores['cantidad'] = [
                'La cantidad debe ser mayor a cero.'
            ]

    except (ValueError, TypeError):
        cantidad = None
        errores['cantidad'] = [
            'Ingresa una cantidad válida.'
        ]

    paciente = None

    if not paciente_documento:
        errores['paciente_documento'] = [
            'Selecciona un paciente.'
        ]
    else:
        paciente = next(
            (
                usuario for usuario in Usuario.objects.all()
                if usuario.documento == paciente_documento
                and usuario.rol
                and usuario.rol['nombre'] == 'Paciente'
            ),
            None
        )

        if paciente is None:
            errores['paciente_documento'] = [
                'El paciente seleccionado no está registrado.'
            ]

    medico = None

    if not medico_documento:
        errores['medico_documento'] = [
            'Selecciona un profesional de salud.'
        ]
    else:
        medico = next(
            (
                usuario for usuario in Usuario.objects.all()
                if usuario.documento == medico_documento
                and usuario.rol
                and usuario.rol['nombre'] in (
                    'Medico', 'Enfermero', 'Farmaceuta'
                )
            ),
            None
        )

        if medico is None:
            errores['medico_documento'] = [
                'El profesional seleccionado no está registrado.'
            ]

    medicamento = None

    if not medicamento_codigo:
        errores['medicamento_codigo'] = [
            'Selecciona un medicamento.'
        ]
    else:
        medicamento = Medicamento.objects.filter(
            codigo=medicamento_codigo
        ).first()

        if medicamento is None:
            errores['medicamento_codigo'] = [
                'El medicamento seleccionado no existe.'
            ]

    return {
        'paciente': paciente,
        'medico': medico,
        'medicamento': medicamento,
        'cantidad': cantidad,
        'observacion': observacion,
    }, errores


@login_requerido
def inicio_dispensacion(request):
    return redirect('find_dispensacion')


@login_requerido
def create_dispensacion(request):

    dispensacion_vacia = {
        'cantidad': '',
        'observacion': '',
        'paciente': {
            'documento': '',
            'nombre': '',
        },
        'medico': {
            'documento': '',
            'nombre': '',
            'rol': '',
        },
        'medicamento': {
            'codigo': '',
            'nombre': '',
            'precio': '',
        }
    }

    if request.method == 'POST':

        datos, errores = _datos_dispensacion(request)

        if not errores:

            medicamento = datos['medicamento']
            cantidad = datos['cantidad']

            if cantidad > medicamento.stock:
                errores['cantidad'] = [
                    f'Stock insuficiente. '
                    f'Solo hay {medicamento.stock} unidades disponibles.'
                ]

        if not errores:

            data = Dispensacion(
                cantidad=datos['cantidad'],
                observacion=datos['observacion'],

                paciente={
                    'documento': datos['paciente'].documento,
                    'nombre': datos['paciente'].nombre,
                },

                medico={
                    'documento': datos['medico'].documento,
                    'nombre': datos['medico'].nombre,
                    'rol': datos['medico'].rol['nombre'],
                },

                medicamento={
                    'codigo': datos['medicamento'].codigo,
                    'nombre': datos['medicamento'].nombre,
                    'precio': datos['medicamento'].precio,
                }
            )

            try:
                data.full_clean()
                data.save()

                datos['medicamento'].stock -= datos['cantidad']
                datos['medicamento'].save()

            except ValidationError as error:
                errores['general'] = error.messages

            else:
                return render(
                    request,
                    'dispensaciones/createDispensacion.html',
                    {'dispensacion': data}
                )

        contexto = _formulario_contexto_dispensacion(
            errores=errores
        )

        contexto['dispensacion'] = dispensacion_vacia

        return render(
            request,
            'dispensaciones/formDispensacion.html',
            contexto
        )

    contexto = _formulario_contexto_dispensacion()
    contexto['dispensacion'] = dispensacion_vacia

    return render(
        request,
        'dispensaciones/formDispensacion.html',
        contexto
    )
    

@login_requerido
def find_dispensacion(request):

    data = Dispensacion.objects.all()

    return render(
        request,
        'dispensaciones/findDispensacion.html',
        {'dispensaciones': data}
    )


@login_requerido
def update_dispensacion(request, id):

    data = get_object_or_404(
        Dispensacion,
        _id=ObjectId(id)
    )

    if request.method == 'POST':

        datos, errores = _datos_dispensacion(request)

        medicamento_anterior = Medicamento.objects.filter(codigo=data.medicamento['codigo']).first()

        if medicamento_anterior is None:
            errores['general'] = [
                'No se encuentra el medicamento de la dispensación original.'
            ]

        if not errores:

            medicamento_nuevo = datos['medicamento']
            cantidad_nueva = datos['cantidad']
            cantidad_anterior = data.cantidad

            mismo_medicamento = (
                medicamento_anterior.codigo ==
                medicamento_nuevo.codigo
            )

            if mismo_medicamento:

                stock_disponible = (
                    medicamento_nuevo.stock + cantidad_anterior
                )

                if cantidad_nueva > stock_disponible:
                    errores['cantidad'] = [
                        f'Stock insuficiente. '
                        f'Disponibles para esta actualización: '
                        f'{stock_disponible} unidades.'
                    ]

            elif cantidad_nueva > medicamento_nuevo.stock:

                errores['cantidad'] = [
                    f'Stock insuficiente. '
                    f'Solo hay {medicamento_nuevo.stock} unidades disponibles.'
                ]

        if not errores:

            data.cantidad = cantidad_nueva
            data.observacion = datos['observacion']

            data.paciente = {
                'documento': datos['paciente'].documento,
                'nombre': datos['paciente'].nombre,
            }

            data.medico = {
                'documento': datos['medico'].documento,
                'nombre': datos['medico'].nombre,
                'rol': datos['medico'].rol['nombre'],
            }

            data.medicamento = {
                'codigo': medicamento_nuevo.codigo,
                'nombre': medicamento_nuevo.nombre,
                'precio': medicamento_nuevo.precio,
            }

            try:
                data.full_clean()
                data.save()

                if mismo_medicamento:

                    medicamento_nuevo.stock = (
                        medicamento_nuevo.stock
                        + cantidad_anterior
                        - cantidad_nueva
                    )

                    medicamento_nuevo.save()

                else:

                    medicamento_anterior.stock += cantidad_anterior
                    medicamento_anterior.save()

                    medicamento_nuevo.stock -= cantidad_nueva
                    medicamento_nuevo.save()

            except ValidationError as error:
                errores['general'] = error.messages

            else:
                return render(
                    request,
                    'dispensaciones/updateDispensacion.html',
                    {'dispensacion': data}
                )

        return render(
            request,
            'dispensaciones/formDispensacion.html',
            _formulario_contexto_dispensacion(
                data,
                errores,
                'Editar dispensación'
            )
        )

    return render(
        request,
        'dispensaciones/formDispensacion.html',
        _formulario_contexto_dispensacion(
            data,
            titulo='Editar dispensación'
        )
    )


@login_requerido
def delete_dispensacion(request, id):

    data = get_object_or_404(
        Dispensacion,
        _id=ObjectId(id)
    )

    if request.method == 'POST':

        medicamento = Medicamento.objects.filter(
            codigo=data.medicamento.codigo
        ).first()

        if medicamento is not None:

            medicamento.stock += data.cantidad
            medicamento.save()

        data.delete()

        return render(
            request,
            'dispensaciones/deleteDispensacion.html',
            {
                'dispensacion': data,
                'confirmar': False
            }
        )

    return render(
        request,
        'dispensaciones/deleteDispensacion.html',
        {
            'dispensacion': data,
            'confirmar': True
        }
    )
