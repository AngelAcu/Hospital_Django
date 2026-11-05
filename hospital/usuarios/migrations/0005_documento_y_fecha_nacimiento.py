import importlib

import django.core.validators
from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import migrations, models

import usuarios.models

COLECCION = 'usuarios_usuario'
INDICE_DOCUMENTO = 'documento_unico'

ESQUEMA_ANTERIOR = importlib.import_module('usuarios.migrations.0004_validacion_json_schema').ESQUEMA_USUARIO

ESQUEMA_USUARIO = {
    **ESQUEMA_ANTERIOR,
    'required': ESQUEMA_ANTERIOR['required'] + ['documento'],
    'properties': {
        **ESQUEMA_ANTERIOR['properties'],
        'documento': {'bsonType': 'string', 'pattern': r'^\d{5,15}$'},
        'fecha_nacimiento': {'bsonType': ['date', 'null']},
    },
}


def cifrar_contrasenas(db):
    # Los usuarios creados antes de usar make_password tienen la contraseña en texto plano.
    for doc in db[COLECCION].find({}, {'password': 1}):
        try:
            identify_hasher(doc['password'])
        except ValueError:
            db[COLECCION].update_one({'_id': doc['_id']}, {'$set': {'password': make_password(doc['password'])}})


def aplicar(apps, schema_editor):
    db = schema_editor.connection.connection
    cifrar_contrasenas(db)
    db.command('collMod', COLECCION, validator={'$jsonSchema': ESQUEMA_USUARIO})
    # Índice parcial: los usuarios antiguos sin documento no chocan entre sí.
    db[COLECCION].create_index(
        'documento', unique=True, name=INDICE_DOCUMENTO,
        partialFilterExpression={'documento': {'$gt': ''}},
    )


def revertir(apps, schema_editor):
    db = schema_editor.connection.connection
    db[COLECCION].drop_index(INDICE_DOCUMENTO)
    db.command('collMod', COLECCION, validator={'$jsonSchema': ESQUEMA_ANTERIOR})


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_validacion_json_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='documento',
            field=models.CharField(default='', max_length=15, validators=[django.core.validators.RegexValidator(message='El documento debe tener entre 5 y 15 números, sin puntos ni espacios.', regex='^\\d{5,15}$')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, validators=[usuarios.models.no_futura]),
        ),
        migrations.RunPython(aplicar, revertir),
    ]
