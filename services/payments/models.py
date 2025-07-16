from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from job.models import RepairJob
from user.models import Repairer
from django.db import models
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='wallet'
    )
    bank_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=20)

    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    escrow_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_balance(self):
        return self.available_balance + self.escrow_balance
    def __str__(self):
        return f"Wallet for {self.user.first_name} {self.user.last_name}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('ESCROW_HOLD', 'Escrow Hold'),
        ('ESCROW_RELEASE', 'Escrow Release'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reference = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Escrow(models.Model):
    ESCROW_STATUS = [
        # ('CREATED', 'Created'),
        ('HELD', 'Funds Held'),
        ('RELEASED', 'Funds Released'),
        ('REFUNDED', 'Funds Refunded'),
    ]

    job_id = models.CharField(max_length=36)  # UUID from external system
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ESCROW_STATUS, default='HELD')
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)
