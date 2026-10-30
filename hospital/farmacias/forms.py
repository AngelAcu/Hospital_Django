from django import forms

class FormularioFarmacias(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    descripcion = forms.CharField(label="Descripcion", max_length=255)
    stock = forms.IntegerField(label="Stock")
    precio = forms.FloatField(label="Precio")
    fecha_vencimiento = forms.DateField(label="Fecha de vencimiento")
    codigo = forms.CharField(label="Codigo", max_length=50)