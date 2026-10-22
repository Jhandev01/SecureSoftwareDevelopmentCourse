from django.conf import settings
from django.db import models


class Incident(models.Model):
    """Incidente reportado por un usuario. Cada incidente tiene UN dueño."""

    class Severity(models.TextChoices):
        LOW = 'low', 'Baja'
        MEDIUM = 'medium', 'Media'
        HIGH = 'high', 'Alta'
        CRITICAL = 'critical', 'Crítica'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incidents'
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=Severity.choices,
                                default=Severity.MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'#{self.pk} {self.title} ({self.owner})'