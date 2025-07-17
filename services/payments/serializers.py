from rest_framework import serializers

from services.payments.models import Wallet, Transaction, Escrow


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['available_balance', 'escrow_balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'tx_type', 'reference', 'created_at']

class EscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escrow
        fields = ['job_id', 'amount', 'status']