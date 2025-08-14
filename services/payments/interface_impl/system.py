from datetime import datetime

from job.models import RepairJob
from services.payments.interfaces import SystemPaymentInterface
from services.payments.models import Wallet, Escrow, Transaction
from user.models import Customer


class SystemPaymentServiceImpl(SystemPaymentInterface):
    def create_escrow(self, job_id: str, bid_amount: float) -> str:

        user_id = RepairJob.objects.get(id=job_id).customer.id
        wallet: Wallet = Wallet.objects.get(user_id=user_id)

        # should have done this while the repairer is bidding
        # if wallet is None:
        #     wallet = Wallet.objects.create(user_id=user_id)

        if wallet.available_balance < bid_amount:
            raise ValueError("Insufficient funds")

        wallet.available_balance -= bid_amount
        wallet.escrow_balance += bid_amount
        wallet.save()

        escrow_id = Escrow.objects.create(
            job_id=job_id,
            # repairer_wallet_id=
            amount=bid_amount,
            status='HELD'
        ).id

        Transaction.objects.create(
            wallet=wallet.id,
            amount=-bid_amount,
            transaction_type='ESCROW_HOLD',
            reference=f"ESCROW_HOLD_{job_id}"
        )

        return str(escrow_id)

    def release_escrow(self, escrow_id: str) -> bool:
        try:
            escrow = Escrow.objects.get(id=escrow_id)
            job = RepairJob.objects.get(id=escrow.job_id)

            repairer_wallet = Wallet.objects.get(user_id=job.selected_bid.repairer.id)

            # should have done this while the repairer is bidding
            if repairer_wallet is None:
                repairer_wallet = Wallet.objects.create(user_id=job.selected_bid.repairer.id)

            repairer_wallet.escrow_balance -= escrow.amount
            repairer_wallet.available_balance += escrow.amount
            repairer_wallet.save()

            Transaction.objects.create(
                wallet=repairer_wallet.id,
                amount=escrow.amount,
                transaction_type='ESCROW_RELEASE',
                reference=f"ESCROW_RELEASE_{escrow.job_id}"
            )

            escrow.status = 'RELEASED'
            escrow.released_at = datetime.now()
            escrow.save()
            return True
        except Escrow.DoesNotExist:
            return False

    @classmethod
    def _initiate_wallet_refund(cls, job_id: str, amount: float) -> None:
        escrow: Escrow = Escrow.objects.get(job_id=job_id)
        job: RepairJob = RepairJob.objects.get(id=escrow.job_id)
        customer_id = job.customer.id
        customer = Customer.objects.get(id=customer_id)
        # wallet:Wallet = Wallet.objects.get(user_id=customer_id)
        wallet: Wallet = Wallet.objects.get(user=customer)

        wallet.available_balance += amount
        escrow.amount -= amount
        wallet.save()
        escrow.save()

    def cancel_escrow(self, escrow_id: str) -> bool:
        try:
            escrow = Escrow.objects.get(id=escrow_id)
            job: RepairJob = RepairJob.objects.get(id=escrow.job_id)

            self._initiate_wallet_refund(
                job_id=str(job.id),
                amount=float(escrow.amount)
            )
            escrow.status = 'REFUNDED'
            escrow.released_at = datetime.now()
            escrow.save()
            return True
        except Escrow.DoesNotExist:
            return False

    def process_withdrawal(self, user_id: str, amount: float) -> str:
        try:  # i get the user
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                wallet = Wallet.objects.get(user=user)
                # check for sufficent funds
                if wallet.available_balance < amount:
                    raise ValueError("Insufficient funds")
                #  debit the wallet
                wallet.available_balance -= amount
                wallet.save()
                # record the withdrawal as pending
                pending_transaction = Transaction.objects.create(
                    wallet=wallet,
                    amount=-amount,
                    transaction_type='WITHDRAWAL',
                    reference=f"WITHDRAWAL_{user_id} - PENDING")
                pending_transaction_id = pending_transaction.id

                # Initiate bank transfer
                transfer_successful: bool = self.process_transfer(
                    transfer_id=str(pending_transaction_id),
                    amount=amount,
                    bank_code=wallet.bank_name,
                    bank_account=wallet.bank_account_number
                )

                if not transfer_successful:
                    raise BankTransferFailedError("Bank transfer initiation failed")

                pending_transaction.reference = f"WITHDRAWAL_{user_id} - SUCCESSFUL"
                pending_transaction.save()
                return f"withdraw_{user_id}_{pending_transaction_id}"
        except User.DoesNotExist:
            return "User does not exist"
        except Wallet.DoesNotExist:
            return "Wallet does not exist"
        except InsufficientFundsError as e:
            return str(e)
        except BankTransferFailedError as e:
            return str(e)
        except Exception as e:
            return f"An unexpected error occurred: {e}"
