from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from djongo import models

ROLES = [
    ('Administrador','Administrador'),
    ('Medico','Medico'),
    ('Enfermero','Enfermero'),
    ('Farmaceuta','Farmaceuta'),
    ('Paciente','Paciente'),
]

solo_numeros = RegexValidator(
    regex=r'^\d{7,15}$',
    message= 'El telefono debe tener entre 7 y 15 números, sin espacions ni letras'
)
usuario_valdio = RegexValidator(
    regex=r'^[a-zA-Z0-9_]+$',
    message= 'El usuario solo puede tener letras,numeros y guion abajo (_).'
)
documento_valido = RegexValidator(
    regex=r'^\d{5,15}$',
    message='El documento debe tener entre 5 y 15 números, sin puntos ni espacios.'
)


def no_futura(fecha):
    if fecha > date.today():
        raise ValidationError('La fecha de nacimiento no puede ser futura.')


class Rol(models.Model):
    nombre = models.CharField(max_length=50, choices=ROLES)
    descripcion = models.CharField(max_length=200)

    class Meta:
        abstract = True
class Usuario(models.Model):
    nombre = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    usuario = models.CharField(max_length=50, unique=True,validators=[MinLengthValidator(3),usuario_valdio])
    password = models.CharField(max_length=128)
    telefono = models.CharField(max_length=15, blank=True, validators=[solo_numeros])
    rol = models.EmbeddedField(model_container=Rol)
    # Sin unique=True: los usuarios creados antes no tienen documento y MongoDB los vería repetidos.
    # La unicidad la revisan clean() y un índice parcial de MongoDB (migración 0005).
    documento = models.CharField(max_length=15, validators=[documento_valido])
    fecha_nacimiento = models.DateField(null=True, blank=True, validators=[no_futura])

    def es_paciente(self):
        return bool(self.rol) and self.rol['nombre'] == 'Paciente'

    def clean(self):
        errores = {}
        if self.documento:
            repetidos = Usuario.objects.filter(documento=self.documento)
            if self.id:
                repetidos = repetidos.exclude(id=self.id)
            if repetidos.count():
                errores['documento'] = 'Ya existe un usuario con este documento.'
        if self.es_paciente() and not self.fecha_nacimiento:
            errores['fecha_nacimiento'] = 'La fecha de nacimiento es obligatoria para los pacientes.'
        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return self.usuario