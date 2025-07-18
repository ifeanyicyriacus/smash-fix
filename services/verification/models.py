from django.db import models
from django.conf import settings


class VerificationRecord(models.Model):
    VERIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('FAILED', 'Failed'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    nin_status = models.CharField(
        max_length=10, choices=VERIFICATION_STATUS, default='PENDING')
    bank_account_status = models.CharField(
        max_length=10, choices=VERIFICATION_STATUS, default='PENDING')
    work_address_status = models.CharField(
        max_length=10, choices=VERIFICATION_STATUS, default='PENDING')
    work_address_verification_reference_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)