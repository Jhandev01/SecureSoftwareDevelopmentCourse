from rest_framework import serializers

from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    """Allowlist explícita de campos (nunca fields = '__all__')."""

    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Incident
        fields = ['id', 'title', 'description', 'severity', 'owner', 'created_at']
        read_only_fields = fields