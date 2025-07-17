from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from services.payments.models import Wallet
from services.payments.service import PaymentService

from .serializers import WalletSerializer, TransactionSerializer

class WalletView:
    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WithdrawView(APIView):
    def post(self, request):
        user_id = request.user.id
        amount = request.data.get('amount')
        service = PaymentService()
        reference = service.payment_gateway.process_withdrawal(
            user_id,
            amount
        )
        return Response(
            {'reference': reference},
            status=status.HTTP_202_ACCEPTED
        )

class TransactionHistoryView(APIView):
    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        transactions = wallet.transactions.order_by('-created_at')[:50]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
