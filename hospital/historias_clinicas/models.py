from django.core.exceptions import ValidationError
from djongo import models

from usuarios.models import Usuario


class PacienteHistoria(models.Model):
    """Ya no se usa: solo existe porque la migración 0001 la importa."""
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)

    class Meta:
        abstract = True


class HistoriaClinica(models.Model):
    # Una historia por paciente, y el paciente debe ser un usuario registrado.
    # PROTECT: no se puede borrar un usuario que tiene historia clínica.
    paciente = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name='historia_clinica')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    antecedentes = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def clean(self):
        try:
            paciente = self.paciente
        except Usuario.DoesNotExist:
            return  # La validación del campo ya informa que falta o no existe.
        if not paciente.es_paciente():
            raise ValidationError({'paciente': 'El usuario seleccionado no tiene el rol Paciente.'})
        # Usuarios creados antes de pedir estos datos pueden no tenerlos.
        if not paciente.documento or not paciente.fecha_nacimiento:
            raise ValidationError({'paciente': 'Completa el documento y la fecha de nacimiento del paciente en Usuarios antes de abrir su historia.'})

    def __str__(self):
        return f'Historia {self.id} - {self.paciente}'
