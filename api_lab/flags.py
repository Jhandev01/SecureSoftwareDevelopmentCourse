"""
api_lab/flags.py

Feature flag que controla la exposición de los endpoints INTENCIONALMENTE
vulnerables (/api/v1/...).

Por defecto el flag está APAGADO (fail-safe default): si nadie lo activa
explícitamente, los endpoints vulnerables no existen.

Solo se activa en local:
    export ENABLE_VULNERABLE_API=True       # Git Bash / Linux / macOS
    $env:ENABLE_VULNERABLE_API="True"       # PowerShell

Nunca se activa en Render (producción).
"""
from functools import wraps

from django.conf import settings
from django.http import JsonResponse


def vulnerable_endpoint(view):
    """
    Decorador para endpoints vulnerables del laboratorio.

    Si el flag está apagado responde 404, igual que una ruta que no existe:
    no revela que el endpoint está ahí.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not getattr(settings, 'ENABLE_VULNERABLE_API', False):
            return JsonResponse({'detail': 'Not found.'}, status=404)
        return view(request, *args, **kwargs)
    return wrapper