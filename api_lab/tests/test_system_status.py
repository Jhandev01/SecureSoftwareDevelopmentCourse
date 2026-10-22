from django.test import TestCase, override_settings

V1 = '/api/v1/system/status/'
V2 = '/api/v2/system/status/'

LEAKY_FIELDS = ['secret_key', 'debug', 'django_version', 'python_version',
                'database', 'allowed_hosts', 'environment_variables']


class SystemStatusV1Tests(TestCase):
    """Documenta la vulnerabilidad: v1 filtra configuración interna."""

    @override_settings(ENABLE_VULNERABLE_API=False)
    def test_v1_hidden_when_flag_off(self):
        self.assertEqual(self.client.get(V1).status_code, 404)

    @override_settings(ENABLE_VULNERABLE_API=True)
    def test_v1_leaks_internal_configuration_to_anonymous(self):
        res = self.client.get(V1)
        self.assertEqual(res.status_code, 200)
        for field in LEAKY_FIELDS:
            self.assertIn(field, res.json())


class SystemStatusV2Tests(TestCase):
    """Verifica la corrección: v2 es público pero no filtra nada."""

    def test_v2_is_public_and_healthy(self):
        res = self.client.get(V2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'status': 'ok'})

    def test_v2_does_not_leak_configuration(self):
        body = self.client.get(V2).json()
        for field in LEAKY_FIELDS:
            self.assertNotIn(field, body)

    @override_settings(ENABLE_VULNERABLE_API=False)
    def test_v2_available_even_with_flag_off(self):
        self.assertEqual(self.client.get(V2).status_code, 200)