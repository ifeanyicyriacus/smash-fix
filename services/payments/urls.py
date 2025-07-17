from django.urls import path
from .views import WalletView, WithdrawView, TransactionHistoryView

urlpatterns = [
    path('wallet/', WalletView.as_view(), name='wallet-detail'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw-funds'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction-history'),
]