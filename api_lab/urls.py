"""
api_lab/urls.py  ->  todas las rutas cuelgan de /api/

  /api/auth/token/  obtener token (POST username + password)
  /api/v1/...       VULNERABLE (solo con ENABLE_VULNERABLE_API=True)
  /api/v2/...       CORREGIDA
"""
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from . import views_v1

# Endpoints VULNERABLES: cada vista lleva @vulnerable_endpoint
v1_patterns = [
    path('system/status/', views_v1.system_status, name='system-status'),
]

# Endpoints CORREGIDOS
v2_patterns = []

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api-token'),
    path('v1/', include((v1_patterns, 'v1'))),
    path('v2/', include((v2_patterns, 'v2'))),
]