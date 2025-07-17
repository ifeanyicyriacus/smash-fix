from rest_framework import serializers

from services.logistics.models import LogisticsAssignment


class LogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsAssignment
        fields = ['job_id', 'status', 'tracking_url']