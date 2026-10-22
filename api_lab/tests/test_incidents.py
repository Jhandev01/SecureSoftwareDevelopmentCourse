from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api_lab.models import Incident


class IncidentBase(TestCase):

    def setUp(self):
        alice = User.objects.create_user('alice')
        bob = User.objects.create_user('bob')
        self.alice_incident = Incident.objects.create(
            owner=alice, title='Secreto de alice', description='Solo alice',
            severity='critical')
        self.bob_incident = Incident.objects.create(
            owner=bob, title='Incidente de bob', description='Solo bob', severity='low')
        self.anon = APIClient()
        self.alice = self._client_for(alice)
        self.bob = self._client_for(bob)

    @staticmethod
    def _client_for(user):
        client = APIClient()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client


@override_settings(ENABLE_VULNERABLE_API=True)
class IncidentV1Tests(IncidentBase):
    """Documenta la vulnerabilidad: el listado es correcto, el detalle no."""

    def test_v1_list_only_shows_own_incidents(self):
        ids = [i['id'] for i in self.bob.get('/api/v1/incidents/').json()]
        self.assertEqual(ids, [self.bob_incident.pk])

    def test_v1_bola_bob_reads_alice_incident(self):
        res = self.bob.get(f'/api/v1/incidents/{self.alice_incident.pk}/')
        self.assertEqual(res.status_code, 200)  # VULNERABLE: debería ser 404
        self.assertEqual(res.json()['owner'], 'alice')