from djongo import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    class Meta:
        abstract = True

class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    usuario = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.EmbeddedField(model_container=Rol)
