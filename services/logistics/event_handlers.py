from common.event_bus import EventBus
from job.events import JobStatusRepairedEvent
from services.logistics.interfaces import LogisticsProviderInterface
from services.logistics.mocks import ClickNShipLogisticsInterface
from services.payments.events import EscrowCreatedEvent


class LogisticsEventHandler:
    """Handles logistics-related events for the job system."""

    def __init__(self, logistics_service: LogisticsProviderInterface = None):
        self.logistics_service = logistics_service or ClickNShipLogisticsInterface()

    def handle_escrow_created(self, event: EscrowCreatedEvent):
        """Handle escrow created event by assigning pickup courier."""
        order_details = {
            "job_id": event.job_id,
            "pickup_type": "1"  # Standard pickup
        }
        self.logistics_service.create_pickup_request(order_details)

    #  todo issue is where do i handle or pass in the payload for logistics pickup request
    def handle_job_repaired(self, event: JobStatusRepairedEvent):
        """Handle job repaired event by assigning delivery courier."""
        order_details = {
            "job_id": event.job_id,
            "pickup_type": "1"  # Standard delivery
        }
        self.logistics_service.create_pickup_request(order_details)

    def subscribe_to_events(self):
        """Register this handler for relevant events."""
        EventBus.subscribe(EscrowCreatedEvent, self.handle_escrow_created)
        EventBus.subscribe(JobStatusRepairedEvent, self.handle_job_repaired)


def register_handlers():
    """Initialize and register logistics event handlers."""
    logistics_handler = LogisticsEventHandler()
    logistics_handler.subscribe_to_events()
