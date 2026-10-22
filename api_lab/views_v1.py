"""
api_lab/views_v1.py

ENDPOINTS INTENCIONALMENTE VULNERABLES - SOLO PARA FINES EDUCATIVOS.
Cada vista está protegida por @vulnerable_endpoint: no existe salvo que
ENABLE_VULNERABLE_API=True. Comparar cada vista con su par en views_v2.py.
"""
import os

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .flags import vulnerable_endpoint
from .system import runtime_details


# ---------------------------------------------------------------------------
# VULN - OWASP API8:2023 Security Misconfiguration
# Un health check público que "de paso" devuelve todo lo que sabe del sistema:
# versiones exactas (-> buscar CVEs), DEBUG activo, ruta de la base de datos,
# hosts permitidos, nombres de variables de entorno y la SECRET_KEY de Django.
# ---------------------------------------------------------------------------
@vulnerable_endpoint
@api_view(['GET'])
@permission_classes([AllowAny])
def system_status(request):
    """
    VULNERABLE: expone configuración interna a cualquier persona.
    Fix (ver v2): un endpoint público responde solo lo que el consumidor
    necesita saber: ¿el servicio está arriba o no?
    """
    return Response({
        'status': 'ok',
        **runtime_details(),
        'debug': settings.DEBUG,                             # MAL: debug visible
        'allowed_hosts': settings.ALLOWED_HOSTS,             # MAL: mapa de hosts
        'secret_key': settings.SECRET_KEY,                   # MUY MAL: secreto
        'environment_variables': sorted(os.environ.keys()),  # MAL: servicios usados
    })