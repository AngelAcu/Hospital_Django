from djongo import models

class ConceptoFactura(models.Model):
    descripcion = models.TextField(blank=True, null=True)
    valor = models.FloatField()

    class Meta:
        abstract = True

class DatosPacienteFactura(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)

    class Meta:
        abstract = True

class Factura(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    estado = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=30, unique=True)
    paciente = models.EmbeddedField(model_container=DatosPacienteFactura)
    conceptos = models.ArrayField(model_container=ConceptoFactura)