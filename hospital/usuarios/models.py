from djongo import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    
class Rol(models.Model):
    nombre: models.CharField(max_length=200)
    
    # Modelo embebido: permite almacenar los datos del modelo
    usuario: models.EmbeddedField(
        model_container=Usuario
    )
