from djongo import models
    
class PacienteDispensacion(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)

    class Meta:
        abstract = True

class MedicamentoDispensacion(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    
    class Meta:
        abstract = True

class Dispensacion(models.Model):
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)
    paciente = models.EmbeddedField(model_container=PacienteDispensacion)
    medicamento = models.EmbeddedField(model_container=MedicamentoDispensacion)
    
class Medicamento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    stock = models.IntegerField(default=0)
    precio = models.FloatField()
    fecha_vencimiento = models.DateField()
    codigo = models.CharField(max_length=50,unique=True)