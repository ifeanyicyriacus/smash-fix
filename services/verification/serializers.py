from rest_framework import serializers

from services.verification.models import VerificationRecord


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRecord
        fields = ['user', 'nin_status', 'bank_account_status', 'work_address_status']
