from django.conf import settings

from job.models import RepairJob
from .interfaces import PaymentGatewayInterface, EscrowInterface
from .mocks import MockEscrowService, MockPaymentGateway

class SquadcoPaymentGateway(PaymentGatewayInterface):

    def _generate_payment_link(self) -> str:
        pass #pass in transaction id, callback_url, amount_in_kobo

    def _generate_payment_callback_url(self) -> str:
        pass

    def _generate_payment_callback_uri(self) -> str:
        pass

    def _verify_payment_callback(self) -> bool:
        # call the escrowCreated event
        pass

    def accept_payment(self, job_id: str, amount: float) -> str:
        # this generate payment link (job_id,
        # successful payment callback our verifier via a REST Get call
        # the REST GET URI will be passed to the payment link verifier
        pass

    def process_transfer(self, job_id: str, amount: float, bank_code: str, bank_account: str):
        pass

    def initiate_refund(self, job_id: str, amount: float):
        pass

    def process_withdrawal(self, user_id: str, amount: float) -> str:
        pass


class SystemEscrowServiceImpl(EscrowInterface):
    def create_escrow(self, job_id: str, bid_amount: float) -> str:

        user_id = RepairJob.objects.get(id=job_id).customer.id
        wallet = Wallet.objects.get(user_id=user_id)

        if wallet.available_balance < bid_amount:
            raise ValueError("Insufficient funds")

        wallet.available_balance -= bid_amount
        wallet.escrow_balance += bid_amount
        wallet.save()

        escrow_id = Escrow.objects.create(
            job_id=job_id,
            amount=bid_amount,
            status='HELD'
        ).id

        Transaction.objects.create(
            wallet=wallet,
            amount=-bid_amount,
            transaction_type='ESCROW_HOLD',
            reference=f"ESCROW_HOLD_{job_id}"
        )

        return str(escrow_id)

    def release_escrow(self, escrow_id: str) -> bool:
        escrow = Escrow.objects.get(id=escrow_id)
        job = RepairJob.objects.get(id=escrow.job_id)

        pass

    def cancel_escrow(self, escrow_id: str) -> bool:
        pass


class PaymentService:
    def __init__(self):
        if settings.USE_SERVICE_MOCKS:
            self.payment_gateway = MockPaymentGateway()
        else:
            self.payment_gateway = SquadcoPaymentGateway()

class EscrowService:
    def __init__(self):
        if settings.USE_SERVICE_MOCKS:
            self.escrow_service = MockEscrowService()
        else:
            self.escrow_service = SystemEscrowServiceImpl()


from .models import Wallet, Escrow, Transaction
from .interfaces import PaymentGatewayInterface
from .mocks import MockPaymentGateway


    def release_escrow(self, escrow: Escrow):
        # Release funds with gateway
        success = self.gateway.release_escrow(escrow.escrow_id)

        if success:
            # Get recipient's wallet
            # In real system, this would come from the job/technician relationship
            wallet = Wallet.objects.get(user_id=escrow.job.technician_id)

            # Update balances
            wallet.available_balance += escrow.amount
            wallet.save()

            # Create transaction
            Transaction.objects.create(
                wallet=wallet,
                amount=escrow.amount,
                transaction_type='ESCROW_RELEASE',
                reference=f"ESCROW_RELEASE_{escrow.job_id}"
            )

            # Update escrow status
            escrow.status = 'RELEASED'
            escrow.save()

            return True
        return False

    def withdraw_funds(self, user_id: str, amount: float):
        wallet = Wallet.objects.get(user_id=user_id)

        if wallet.available_balance < amount:
            raise ValueError("Insufficient funds")

        # Process withdrawal
        reference = self.gateway.process_withdrawal(user_id, amount)

        # Update balance
        wallet.available_balance -= amount
        wallet.save()

        # Create transaction
        Transaction.objects.create(
            wallet=wallet,
            amount=-amount,
            transaction_type='WITHDRAWAL',
            reference=reference
        )

        return reference