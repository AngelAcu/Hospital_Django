from djongo import models
    
class PacienteDispensacion(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)

    class Meta:
        abstract = True
        
class MedicoDispensacion(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)
    rol = models.CharField(max_length=100)

    class Meta:
        abstract = True

class MedicamentoDispensacion(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    
    class Meta:
        abstract = True

class Dispensacion(models.Model):
    _id = models.ObjectIdField()
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)
    paciente = models.EmbeddedField(model_container=PacienteDispensacion)
    medicamento = models.EmbeddedField(model_container=MedicamentoDispensacion)
    medico = models.EmbeddedField(model_container=MedicoDispensacion)
    
    @property
    def id(self):
        return str(self._id)
    
class Medicamento(models.Model):
    _id = models.ObjectIdField()
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    stock = models.IntegerField(default=0)
    precio = models.FloatField()
    fecha_vencimiento = models.DateField()
    codigo = models.CharField(max_length=50,unique=True)
    
    @property
    def id(self):
        return str(self._id)