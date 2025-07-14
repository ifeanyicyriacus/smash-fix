from django.conf import settings

from .interfaces import PaymentGatewayInterface, EscrowInterface
from .mocks import MockEscrowInterface

class SquadcoPaymentService(PaymentGatewayInterface):

    def accept_payment(self, job_id: str, amount: float):
        pass

    def process_transfer(self, job_id: str, amount: float, bank_code: str, bank_account: str):
        pass

    def initiate_refund(self, job_id: str, amount: float):
        pass


class EscrowService(EscrowInterface):

    def create_escrow(self, job_id: str, bid_amount: float) -> str:
        pass

    def release_escrow(self, escrow_id: str) -> bool:
        pass

    def cancel_escrow(self, escrow_id: str) -> bool:
        pass


class PaymentService:
    def __init__(self):
        if settings.USE_SERVICE_MOCKS:
            self.gateway = MockEscrowInterface()
        else:
            self.gateway = SquadcoPaymentService()