
from common.event_bus import EventBus


class EventHandlerRegistry:
    """Central registry for event handlers with lazy loading to avoid circular imports."""

    @classmethod
    def register_handlers(cls) -> None:
        """Register all event handlers with the event bus."""
        # Lazy import to avoid circular dependencies
        from services.payments.event_handlers import EscrowEventHandler
        from services.logistics.event_handlers import LogisticsEventHandler
        from services.notifications.event_handlers import NotificationsEventHandler
        from job.events import (
            JobCreatedEvent, BidAcceptedEvent, JobStatusChangedEvent,
            JobAssignedEvent, JobCompletedEvent
        )

        # Initialize handlers only when needed
        escrow_handler = EscrowEventHandler()
        logistics_handler = LogisticsEventHandler()
        notifications_handler = NotificationsEventHandler()

        # Register event handlers
        EventBus.subscribe(
            JobCreatedEvent,
            notifications_handler.handle_job_created
        )
        EventBus.subscribe(
            BidAcceptedEvent,
            escrow_handler.handle_bid_accepted
        )
        EventBus.subscribe(
            JobStatusChangedEvent,
            escrow_handler.handle_job_status_changed
        )
        EventBus.subscribe(
            JobAssignedEvent,
            logistics_handler.handle_job_assigned
        )
        EventBus.subscribe(
            JobCompletedEvent,
            logistics_handler.handle_job_completed
        )

