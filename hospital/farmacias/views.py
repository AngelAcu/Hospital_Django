
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
from bson import ObjectId

from usuarios.sesion import login_requerido

from .models import Medicamento


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
