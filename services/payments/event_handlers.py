from enum import Enum

from common.event_bus import EventBus
from job.events import BidAcceptedEvent, JobStatusChangedEvent
from services.payments.interfaces import PaymentGatewayInterface, EscrowInterface
from services.payments.mocks import MockPaymentGateway, MockEscrowInterface


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

class EscrowEventHandler:
    """Handles escrow-related events for the job system."""
    def __init__(self, escrow_service: EscrowInterface = None):
        self.escrow_service: EscrowInterface = escrow_service or MockEscrowInterface()


    def handle_bid_accepted(self, event: BidAcceptedEvent):
        #Handler for bid acceptance that creates an escrow for the bid amount
        self.escrow_service.create_escrow(event.job_id, event.bid_amount)
        # NotificationService.send_notification(
        #     event.repairer_id,
        #     "Bid Accepted",
        #     f"Your bid for job #{event.job_id} has been accepted"
        # )

    #     call the payment helper

    #     let notification/event_handler also listen to this and all event


    def handle_job_status_changed(self, event: JobStatusChangedEvent):
        #Handler for job status changes that manages escrow release or cancellation
        if event.new_status == JobStatus.COMPLETED:
            self.escrow_service.release_escrow(event.job_id)
        elif event.new_status in [JobStatus.CANCELLED, JobStatus.EXPIRED]:
            self.escrow_service.cancel_escrow(event.job_id)



#     def subscribe_to_events(self) -> None:
#         """Register this handler for relevant events."""
#         EventBus.subscribe(BidAcceptedEvent, self.handle_bid_accepted)
#         EventBus.subscribe(JobStatusChangedEvent, self.handle_job_status_changed)
#
# def register_handlers():
#     """Initialize and register all event handlers for the payment service."""
#     handler = EscrowEventHandler()
#     handler.subscribe_to_events()
