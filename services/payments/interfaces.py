
from abc import ABC, abstractmethod

class PaymentGatewayInterface(ABC):
    @abstractmethod
    def accept_payment(self, job_id: str, amount: float):
        pass

    @abstractmethod
    def initiate_refund(self, job_id:str, amount:float):
        pass

    @abstractmethod
    def process_transfer(self, job_id:str, amount:float, bank_code:str, bank_account:str):
        pass


class EscrowInterface(ABC):
    @abstractmethod
    def create_escrow(self, job_id: str, bid_amount: float) -> str:
        pass

    @abstractmethod
    def release_escrow(self, escrow_id: str) -> bool:
        pass

    @abstractmethod
    def cancel_escrow(self, escrow_id: str) -> bool:
        pass

