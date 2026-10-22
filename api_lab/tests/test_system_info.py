from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

V1 = '/api/v1/system/info/'
V2 = '/api/v2/system/info/'


class SystemInfoBase(TestCase):

    def setUp(self):
        self.anon = APIClient()
        self.bob = self._client_for(User.objects.create_user('bob'))
        self.profe = self._client_for(User.objects.create_user('profe', is_staff=True))

    @staticmethod
    def _client_for(user):
        client = APIClient()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client


@override_settings(ENABLE_VULNERABLE_API=True)
class SystemInfoV1Tests(SystemInfoBase):
    """Documenta la vulnerabilidad: v1 autentica pero no autoriza."""

    def test_v1_requires_authentication(self):
        self.assertEqual(self.anon.get(V1).status_code, 401)

    def test_v1_regular_user_reaches_admin_function(self):
        res = self.bob.get(V1)
        self.assertEqual(res.status_code, 200)  # VULNERABLE: debería ser 403
        staff = [u['username'] for u in res.json()['users']['staff']]
        self.assertIn('profe', staff)