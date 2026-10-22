from django.contrib.auth.models import User
from django.http import JsonResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from api_lab.flags import vulnerable_endpoint


@vulnerable_endpoint
def dummy_view(request):
    return JsonResponse({'ok': True})


class VulnerableFlagTests(TestCase):
    """El flag debe estar apagado por defecto (fail-safe default)."""

    def setUp(self):
        self.request = RequestFactory().get('/dummy/')

    @override_settings(ENABLE_VULNERABLE_API=False)
    def test_flag_off_returns_404(self):
        self.assertEqual(dummy_view(self.request).status_code, 404)

    @override_settings(ENABLE_VULNERABLE_API=True)
    def test_flag_on_serves_view(self):
        self.assertEqual(dummy_view(self.request).status_code, 200)


class TokenEndpointTests(TestCase):

    def setUp(self):
        User.objects.create_user('alice', password='lab-pass-123')  # nosec B106

    def test_valid_credentials_return_token(self):
        res = self.client.post(reverse('api-token'),
                               {'username': 'alice', 'password': 'lab-pass-123'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.json())

    def test_invalid_credentials_rejected(self):
        res = self.client.post(reverse('api-token'),
                               {'username': 'alice', 'password': 'wrong'})
        self.assertEqual(res.status_code, 400)
        self.assertNotIn('token', res.json())