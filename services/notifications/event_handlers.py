from common.event_bus import EventBus
from job.events import BidAcceptedEvent
from services.payments.events import EscrowCreatedEvent
from services.notifications.interfaces import NotificationInterface
from services.notifications.mocks import MockNotificationService


class NotificationEventHandler:
    """Handles notification-related events for the job system."""

    def __init__(self, notification_service: NotificationInterface = None):
        self.notification_service: NotificationInterface = notification_service or MockNotificationService()

    def handle_bid_accepted(self, event: BidAcceptedEvent):
        """Handle bid accepted event by sending notifications."""
        self.notification_service.send_notification(
            user_id=event.repairer_id,
            message=f"Your bid for job {event.job_id} has been accepted!"
        )

    def handle_escrow_created(self, event: EscrowCreatedEvent):
        """Handle escrow created event by sending notifications."""
        self.notification_service.send_notification(
            job_id=event.job_id,
            message=f"Escrow has been created for amount ${event.amount}"
        )

    def subscribe_to_events(self) -> None:
        """Register this handler for relevant events."""
        EventBus.subscribe(BidAcceptedEvent, self.handle_bid_accepted)
        EventBus.subscribe(EscrowCreatedEvent, self.handle_escrow_created)


def register_handlers():
    """Initialize and register all event handlers for the notification service."""
    handler = NotificationEventHandler()
    handler.subscribe_to_events()
