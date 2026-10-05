from djongo import models

class PacienteHistoria(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)

    class Meta:
        abstract = True

class HistoriaClinica(models.Model):
    paciente = models.EmbeddedField(model_container=PacienteHistoria)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    antecedentes = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
