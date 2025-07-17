from enum import Enum

from common.event_bus import EventBus
from job.events import BidAcceptedEvent, RepairCompletedEvent
from services.payments.events import EscrowCreatedEvent
from services.payments.interfaces import PaymentGatewayInterface, EscrowInterface
from services.payments.mocks import MockPaymentGateway, MockEscrowService
from services.payments.models import Escrow


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
                 payment_service: PaymentGatewayInterface = None,
                 escrow_service: EscrowInterface = None):
        self.escrow_service: EscrowInterface = escrow_service
        self.payment_service: PaymentGatewayInterface = payment_service

    def handle_bid_accepted(self, event:BidAcceptedEvent):
        """Handle bid accepted event by processing the payment."""
        self.escrow_service.create_escrow(
            job_id=event.job_id,
            bid_amount=event.bid_amount
        )

    def handle_repair_completed(self, event:RepairCompletedEvent):
        escrow = Escrow.objects.get(job_id=event.job_id)
        self.escrow_service.release_escrow(escrow)

    def subscribe_to_events(self):
        EventBus.subscribe('BidAcceptedEvent', self.handle_bid_accepted)
        EventBus.subscribe('RepairCompletedEvent', self.handle_repair_completed)


class EscrowEventHandler:
    """Handles escrow-related events for the job system."""
    def __init__(self, escrow_service: EscrowInterface = None):
        self.escrow_service: EscrowInterface = escrow_service or MockEscrowService()
    def handle_job_status_changed(self, event: JobStatusChangedEvent):
        #Handler for job status changes that manages escrow release or cancellation
        escrow:Escrow = Escrow.objects.get(job_id=event.job_id)
        if event.new_status == JobStatus.COMPLETED:
            self.escrow_service.release_escrow(escrow)
        elif event.new_status in [JobStatus.CANCELLED, JobStatus.EXPIRED]:
            self.escrow_service.cancel_escrow(escrow)



    def subscribe_to_events(self) -> None:
        """Register this handler for relevant events."""
        EventBus.subscribe(JobStatusChangedEvent, self.handle_job_status_changed)


def register_handlers():
    """Initialize and register all event handlers for the payment service."""
    escrow_handler = EscrowEventHandler()
    payment_handler = PaymentEventHandler()

    escrow_handler.subscribe_to_events()
    payment_handler.subscribe_to_events()
