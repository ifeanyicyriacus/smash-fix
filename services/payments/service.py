from django.conf import settings

from services.payments.interface_impl.mocks import MockSystemPaymentService, MockPaymentGateway
from .interface_impl.squadco_payment_impl import SquadcoPaymentGateway
from .interface_impl.system import SystemPaymentServiceImpl

class PaymentService:
    def __init__(self):
        if settings.USE_SERVICE_MOCKS:
            self.payment_gateway = MockPaymentGateway()
            self.escrow_service = MockSystemPaymentService()
        else:
            self.payment_gateway = SquadcoPaymentGateway()
            self.escrow_service = SystemPaymentServiceImpl()
