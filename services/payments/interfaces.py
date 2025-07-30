
from abc import ABC, abstractmethod

from services.payments.models import Escrow


class PaymentGatewayInterface(ABC):
    @abstractmethod
    def accept_payment(self, job_id: str, amount: float):
        pass

    @abstractmethod
    def process_transfer(self, job_id:str, amount:float, bank_code:str, bank_account:str):
        pass

class SystemPaymentInterface(ABC):
    @abstractmethod
    def create_escrow(self, job_id: str, bid_amount: float) -> str:
        pass

    @abstractmethod
    def release_escrow(self, escrow: Escrow) -> bool:
        pass

    @abstractmethod
    def cancel_escrow(self, escrow: Escrow) -> bool:
        pass

    @abstractmethod
    def process_withdrawal(self, user_id: str, amount: float) -> str:
        pass

class PaymentServiceInterface(PaymentGatewayInterface, SystemPaymentInterface, ABC):
    pass