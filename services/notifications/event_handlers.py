from common.event_bus import EventBus
from job.events import BidAcceptedEvent
from user.models import Customer
from .service import NotificationService
from services.payments.events import EscrowCreatedEvent

notification_service = NotificationService()

def handle_bid_accepted(event: BidAcceptedEvent):
    """Handle bid accepted event by sending notifications."""
    notification_service.create_notification(
        user_id=event.repairer_id,
        title="Bid Accepted",
        message=f"Your bid for job {event.job_id} has been accepted!",
        notification_type="BID_UPDATE",
        notification_medium="ALL"
    )
    # notify customer of repair schedule
    customer_id = Customer.objects.get(job_id=event.job_id).id
    notification_service.create_notification(
        user_id=customer_id,
        title="Repair Scheduled",
        message=f"Your repair for job #{event.job_id} has been scheduled!",
        notification_type="JOB_UPDATE",
        notification_medium="ALL"
    )

def handle_escrow_created(event: EscrowCreatedEvent):
    """Handle escrow created event by sending notifications."""
    customer_id = Customer.objects.get(job_id=event.job_id).id
    notification_service.create_notification(
        user_id=customer_id,
        title="Payment Processed",
        message=f"Your payment for job #{event.job_id} has been secured in escrow",
        notification_type="JOB_UPDATE",
        notification_medium="ALL"
    )

def register_handlers():
    """Initialize and register all event handlers for the notification service."""
    EventBus.subscribe(BidAcceptedEvent, handle_bid_accepted)
    EventBus.subscribe(EscrowCreatedEvent, handle_escrow_created)
