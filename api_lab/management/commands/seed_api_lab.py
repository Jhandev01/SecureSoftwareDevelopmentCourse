"""
python manage.py seed_api_lab

Crea los usuarios del laboratorio y muestra sus tokens:
    alice  -> usuaria normal
    bob    -> usuario normal (el "atacante" de los ejercicios)
    profe  -> administrador (is_staff)

Las contraseñas se generan al azar en cada ejecución (nada hardcodeado en el repo).
Solo corre si ENABLE_VULNERABLE_API=True, para que nunca siembre usuarios de
prueba en producción.
"""
import secrets

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token

from api_lab.models import Incident

LAB_INCIDENTS = [
    # (owner, title, description, severity)
    ('alice', 'Credenciales de BD en logs de la app',
     'El log de errores imprime la cadena de conexión completa con usuario y password.',
     'critical'),
    ('alice', 'Certificado TLS del portal vence en 10 días',
     'portal.empresa.local usa un certificado que expira pronto.', 'medium'),
    ('bob', 'Puerto 22 abierto en servidor de pruebas',
     'SSH expuesto a internet en el servidor de QA.', 'high'),
    ('profe', 'Revisión trimestral de accesos pendiente',
     'Falta revisar cuentas inactivas de exalumnos en el repositorio.', 'low'),
]

LAB_USERS = [
    # (username, email, is_staff)
    ('alice', 'alice@lab.local', False),
    ('bob', 'bob@lab.local', False),
    ('profe', 'profe@lab.local', True),
]


class Command(BaseCommand):
    help = 'Crea usuarios y tokens para el laboratorio de APIs (solo local).'

    def handle(self, *args, **options):
        if not getattr(settings, 'ENABLE_VULNERABLE_API', False):
            raise CommandError(
                'ENABLE_VULNERABLE_API no está activo. Este comando es solo '
                'para entornos locales de laboratorio.'
            )

        self.stdout.write(self.style.MIGRATE_HEADING('Usuarios del laboratorio'))
        for username, email, is_staff in LAB_USERS:
            user, _ = User.objects.get_or_create(
                username=username, defaults={'email': email}
            )
            user.is_staff = is_staff
            password = secrets.token_urlsafe(12)
            user.set_password(password)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            role = 'admin' if is_staff else 'usuario'
            self.stdout.write(
                f'  {username:<6} ({role:<7})  password: {password}  token: {token.key}'
            )

        self.seed_data()
        done = 'Listo. Usa: -H "Authorization: Token <token>"'
        self.stdout.write(self.style.SUCCESS(done))

    def seed_data(self):
        """Datos de ejemplo de cada endpoint del laboratorio."""
        self.stdout.write(self.style.MIGRATE_HEADING('Incidentes'))
        for owner, title, description, severity in LAB_INCIDENTS:
            incident, _ = Incident.objects.get_or_create(
                owner=User.objects.get(username=owner), title=title,
                defaults={'description': description, 'severity': severity},
            )
            self.stdout.write(f'  #{incident.pk:<3} {owner:<6} {title}')