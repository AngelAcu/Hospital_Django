from djongo import models

class PacienteCita(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    class Meta:
        abstract = True

class MedicoCita(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Cita(models.Model):
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=300)
    estado = models.CharField(max_length=20)
    paciente = models.EmbeddedField(model_container=PacienteCita)
    medico = models.EmbeddedField(model_container=MedicoCita)