"""
api_lab/system.py

Recolección de información técnica del sistema. Separado de las vistas para que
v1 y v2 usen exactamente la misma fuente: la diferencia entre la versión
vulnerable y la corregida está en QUÉ se expone y A QUIÉN, no en cómo se
obtiene el dato.
"""
import platform
import sys

import django
from django.conf import settings


def runtime_details():
    """Versiones y entorno de ejecución. Información útil para un atacante."""
    db = settings.DATABASES['default']
    return {
        'django_version': django.get_version(),
        'python_version': sys.version,
        'platform': platform.platform(),
        'hostname': platform.node(),
        'database': {'engine': db['ENGINE'], 'name': str(db['NAME'])},
    }