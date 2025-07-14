# from common.event_bus import EventBus
# from job.events import JobCreatedEvent, BidAcceptedEvent, JobStatusChangedEvent
# from services.notifications.interfaces import NotificationService
# from services.logistics.interfaces import LogisticsService
# from services.payments.interfaces import PaymentGatewayInterface, EscrowInterface
#
#
# def handle_job_created(event: JobCreatedEvent):
#     # Notify customer of job creation
#     NotificationService.send_notification(
#         event.customer_id,
#         "Job Created",
#         f"Your repair job #{event.job_id} has been created successfully"
#     )
#
#     # Initialize logistics tracking
#     LogisticsService.initialize_job_tracking(event.job_id)
#
#
# def handle_bid_accepted(event: BidAcceptedEvent):
#     # Setup escrow payment
#     escrow_id = EscrowInterface.create_escrow(event.job_id, event.bid_amount)
#
#     # Notify repairer
#     NotificationService.send_notification(
#         event.repairer_id,
#         "Bid Accepted",
#         f"Your bid for job #{event.job_id} has been accepted"
#     )
#
#
# def handle_job_status_changed(event: JobStatusChangedEvent):
#     if event.new_status == 'COMPLETED':
#         # Release payment from escrow
#         EscrowInterface.release_escrow(event.job_id)
#     elif event.new_status == 'CANCELLED':
#         # Cancel escrow and refund
#         EscrowInterface.cancel_escrow(event.job_id)
#
#
# # Register event handlers
# EventBus.subscribe(JobCreatedEvent, handle_job_created)
# EventBus.subscribe(BidAcceptedEvent, handle_bid_accepted)
# EventBus.subscribe(JobStatusChangedEvent, handle_job_status_changed)
from common.event_bus import EventBus
from job.events import JobCreatedEvent, JobStatusChangedEvent, BidAcceptedEvent


def register_handlers():
    """Initialize and register all event handlers for the job service."""
    EventBus.subscribe(JobCreatedEvent, handle_job_created)
    EventBus.subscribe(BidAcceptedEvent, handle_bid_accepted)
    EventBus.subscribe(JobStatusChangedEvent, handle_job_status_changed)