from django.db import migrations

TEXTO_OPCIONAL = {'bsonType': ['string', 'null']}

ESQUEMA_HISTORIA = {
    'bsonType': 'object',
    'required': ['paciente', 'fecha_creacion'],
    'properties': {
        'paciente': {
            'bsonType': 'object',
            'required': ['documento', 'nombre', 'fecha_nacimiento', 'telefono'],
            'properties': {
                'documento': {'bsonType': 'string', 'pattern': r'^\d{5,15}$'},
                'nombre': {'bsonType': 'string', 'minLength': 3, 'maxLength': 200},
                'fecha_nacimiento': {'bsonType': 'date'},
                'telefono': {'bsonType': 'string', 'pattern': r'^\d{7,15}$'},
            },
        },
        'fecha_creacion': {'bsonType': 'date'},
        'antecedentes': TEXTO_OPCIONAL,
        'alergias': TEXTO_OPCIONAL,
        'observaciones': TEXTO_OPCIONAL,
    },
}

COLECCION = 'historias_clinicas_historiaclinica'
INDICE_DOCUMENTO = 'paciente_documento_unico'


def aplicar_esquema(apps, schema_editor):
    db = schema_editor.connection.connection
    db.command('collMod', COLECCION, validator={'$jsonSchema': ESQUEMA_HISTORIA})
    # Un paciente tiene una sola historia clínica.
    db[COLECCION].create_index('paciente.documento', unique=True, name=INDICE_DOCUMENTO)


def quitar_esquema(apps, schema_editor):
    db = schema_editor.connection.connection
    db.command('collMod', COLECCION, validator={})
    db[COLECCION].drop_index(INDICE_DOCUMENTO)


class Migration(migrations.Migration):

    dependencies = [
        ('historias_clinicas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(aplicar_esquema, quitar_esquema),
    ]
