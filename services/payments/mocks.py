from services.payments.interfaces import PaymentGatewayInterface, EscrowInterface
from typing import Dict
import uuid


class MockPaymentGateway(PaymentGatewayInterface):
    def __init__(self):
        self.transactions: Dict[str, dict] = {}

    def accept_payment(self, job_id: str, amount: float):
        transaction_id = str(uuid.uuid4())
        mock_response = {
            "status": "success",
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": "NGN",
            "payment_status": "completed",
            "job_id": job_id
        }
        self.transactions[transaction_id] = mock_response
        return mock_response

    def initiate_refund(self, job_id: str, amount: float):
        refund_id = str(uuid.uuid4())
        mock_response = {
            "status": "success",
            "refund_id": refund_id,
            "amount": amount,
            "currency": "NGN",
            "refund_status": "processed",
            "job_id": job_id
        }
        self.transactions[refund_id] = mock_response
        return mock_response

    def process_transfer(self, job_id: str, amount: float, bank_code: str, bank_account: str):
        transfer_id = str(uuid.uuid4())
        mock_response = {
            "status": "success",
            "transfer_id": transfer_id,
            "amount": amount,
            "currency": "NGN",
            "transfer_status": "completed",
            "bank_code": bank_code,
            "account_number": bank_account,
            "job_id": job_id
        }
        self.transactions[transfer_id] = mock_response
        return mock_response


class MockEscrowService(EscrowInterface):
    def __init__(self):
        self.escrow_transactions: Dict[str, dict] = {}

    def create_escrow(self, job_id: str, bid_amount: float) -> str:
        escrow_id = str(uuid.uuid4())
        mock_escrow = {
            "escrow_id": escrow_id,
            "job_id": job_id,
            "amount": bid_amount,
            "status": "active",
            "currency": "NGN"
        }
        self.escrow_transactions[escrow_id] = mock_escrow
        return escrow_id

    def release_escrow(self, escrow_id: str) -> bool:
        if escrow_id in self.escrow_transactions:
            self.escrow_transactions[escrow_id]["status"] = "released"
            return True
        return False

    def cancel_escrow(self, escrow_id: str) -> bool:
        if escrow_id in self.escrow_transactions:
            self.escrow_transactions[escrow_id]["status"] = "cancelled"
            return True
        return False
