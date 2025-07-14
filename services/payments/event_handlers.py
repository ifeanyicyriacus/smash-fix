from enum import Enum

from common.event_bus import EventBus
from job.events import BidAcceptedEvent, JobStatusChangedEvent
from services.payments.events import EscrowCreatedEvent
from services.payments.interfaces import PaymentGatewayInterface, EscrowInterface
from services.payments.mocks import MockPaymentGateway, MockEscrowService


class JobStatus(Enum):
    """Enum representing possible job statuses"""
    OPEN = 'OPEN'
    BIDDING = 'BIDDING'
    ASSIGNED = 'ASSIGNED'
    IN_PROGRESS = 'IN_PROGRESS'
    REPAIRED = 'REPAIRED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'

class PaymentEventHandler:
    """Handles payment-related events for the job system."""

    def __init__(self,
                 payment_gateway: PaymentGatewayInterface = None,
                 escrow_service: EscrowInterface = None):
        self.escrow_service: EscrowInterface = escrow_service or MockEscrowService()
        self.payment_gateway: PaymentGatewayInterface = payment_gateway or MockPaymentGateway()

    def handle_bid_accepted(self, event:BidAcceptedEvent):
        """Handle bid accepted event by processing the payment."""
        self.payment_gateway.accept_payment(
            job_id=event.job_id,
            amount=event.bid_amount
        )

        EventBus.subscribe(BidAcceptedEvent, self.handle_bid_accepted)
        escrow_id = self.escrow_service.create_escrow(
            job_id=event.job_id,
            bid_amount=event.bid_amount
        )

        EventBus.publish(EscrowCreatedEvent(
            job_id=event.job_id,
            escrow_id=escrow_id,
            amount=event.bid_amount
        ))


class EscrowEventHandler:
    """Handles escrow-related events for the job system."""
    def __init__(self, escrow_service: EscrowInterface = None):
        self.escrow_service: EscrowInterface = escrow_service or MockEscrowService()

    def handle_job_status_changed(self, event: JobStatusChangedEvent):
        #Handler for job status changes that manages escrow release or cancellation
        if event.new_status == JobStatus.COMPLETED:
            self.escrow_service.release_escrow(event.job_id)
        elif event.new_status in [JobStatus.CANCELLED, JobStatus.EXPIRED]:
            self.escrow_service.cancel_escrow(event.job_id)



    def subscribe_to_events(self) -> None:
        """Register this handler for relevant events."""
        EventBus.subscribe(JobStatusChangedEvent, self.handle_job_status_changed)


def register_handlers():
    """Initialize and register all event handlers for the payment service."""
    escrow_handler = EscrowEventHandler()
    payment_handler = PaymentEventHandler()

    escrow_handler.subscribe_to_events()
    payment_handler.subscribe_to_events()
