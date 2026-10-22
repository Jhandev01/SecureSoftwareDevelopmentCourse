"""
api_lab/views_v2.py

ENDPOINTS CORREGIDOS - comparar cada vista con su par en views_v1.py.
"""
from django.db import DatabaseError, connection
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Incident
from .serializers import IncidentSerializer
from .system import admin_details


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


# ---------------------------------------------------------------------------
# FIX - OWASP API5:2023 Broken Function Level Authorization (BFLA)
# Misma función, mismos datos. La única diferencia con v1 es el permiso:
# la corrección de BFLA suele ser una línea; el problema es olvidarla.
# ---------------------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAdminUser])   # BIEN: solo usuarios is_staff
def system_info(request):
    """
    CORREGIDO: autenticación (token válido) + autorización (rol admin).
    Usuario sin rol -> 403. Sin token -> 401.
    """
    return Response(admin_details())


# ---------------------------------------------------------------------------
# FIX - OWASP API1:2023 Broken Object Level Authorization (BOLA)
# Un único punto define "qué objetos puede ver este usuario" y TODAS las
# vistas parten de ahí (complete mediation, Sesión 2). Si mañana se agrega
# PATCH o DELETE, heredan el mismo filtro.
# ---------------------------------------------------------------------------
def incidents_for(user):
    """Conjunto de incidentes al que el usuario tiene acceso."""
    return Incident.objects.filter(owner=user)


@api_view(['GET'])
def incident_list(request):
    return Response(IncidentSerializer(incidents_for(request.user), many=True).data)


@api_view(['GET'])
def incident_detail(request, pk):
    """
    CORREGIDO: el objeto se busca dentro del conjunto del usuario.
    Un incidente ajeno responde 404 (no 403): no confirmamos que existe.
    """
    incident = get_object_or_404(incidents_for(request.user), pk=pk)   # BIEN
    return Response(IncidentSerializer(incident).data)