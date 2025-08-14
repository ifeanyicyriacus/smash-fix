from services.payments.interfaces import PaymentGatewayInterface


class SquadcoPaymentGateway(PaymentGatewayInterface):

    def _generate_payment_link(self) -> str:
        pass  # pass in transaction id, callback_url, amount_in_kobo

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

    def process_transfer(self, transfer_id: str, amount: float, bank_code: str, bank_account: str) -> bool:
        # finally i return the reference to the transfer
        # make tha API call
        pass
