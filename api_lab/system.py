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


def admin_details():
    """
    Información administrativa: configuración y cuentas privilegiadas.
    Legítima para un administrador; peligrosa en cualquier otra mano.
    Nota: aun para admins NO incluye secretos (SECRET_KEY, variables de entorno).
    """
    from django.contrib.auth.models import User

    staff = User.objects.filter(is_staff=True).order_by('username')
    return {
        **runtime_details(),
        'installed_apps': settings.INSTALLED_APPS,
        'middleware': settings.MIDDLEWARE,
        'users': {
            'total': User.objects.count(),
            'staff': [
                {'username': u.username,
                 'last_login': u.last_login.isoformat() if u.last_login else None}
                for u in staff
            ],
        },
    }