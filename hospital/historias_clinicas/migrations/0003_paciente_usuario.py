import importlib

import django.db.models.deletion
from django.db import migrations, models

COLECCION = 'historias_clinicas_historiaclinica'
INDICE_ANTERIOR = 'paciente_documento_unico'

ANTERIOR = importlib.import_module('historias_clinicas.migrations.0002_validacion_json_schema')

TEXTO_OPCIONAL = {'bsonType': ['string', 'null']}

ESQUEMA_HISTORIA = {
    'bsonType': 'object',
    'required': ['paciente_id', 'fecha_creacion'],
    'properties': {
        'paciente_id': {'bsonType': ['int', 'long']},
        'fecha_creacion': {'bsonType': 'date'},
        'antecedentes': TEXTO_OPCIONAL,
        'alergias': TEXTO_OPCIONAL,
        'observaciones': TEXTO_OPCIONAL,
    },
}


def quitar_esquema_anterior(apps, schema_editor):
    db = schema_editor.connection.connection
    db.command('collMod', COLECCION, validator={})
    db[COLECCION].drop_index(INDICE_ANTERIOR)


def restaurar_esquema_anterior(apps, schema_editor):
    ANTERIOR.aplicar_esquema(apps, schema_editor)


# La regla "una historia por paciente" la crea djongo como índice único al agregar el OneToOneField.
def aplicar_esquema(apps, schema_editor):
    db = schema_editor.connection.connection
    db.command('collMod', COLECCION, validator={'$jsonSchema': ESQUEMA_HISTORIA})


def quitar_esquema(apps, schema_editor):
    db = schema_editor.connection.connection
    db.command('collMod', COLECCION, validator={})


class Migration(migrations.Migration):

    dependencies = [
        ('historias_clinicas', '0002_validacion_json_schema'),
        ('usuarios', '0005_documento_y_fecha_nacimiento'),
    ]

    operations = [
        migrations.RunPython(quitar_esquema_anterior, restaurar_esquema_anterior),
        migrations.RemoveField(
            model_name='historiaclinica',
            name='paciente',
        ),
        migrations.AddField(
            model_name='historiaclinica',
            name='paciente',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='historia_clinica', to='usuarios.usuario'),
            preserve_default=False,
        ),
        migrations.RunPython(aplicar_esquema, quitar_esquema),
    ]
