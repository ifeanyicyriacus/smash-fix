from common.event_bus import EventBus
from job.events import BidAcceptedEvent, JobStatusRepairedEvent
from services.logistics.service import LogisticsService

def handle_bid_accepted(event: BidAcceptedEvent):
    logistics_service = LogisticsService()
    logistics_service.create_pickup_request_for_customer(
        job_id=event.job_id,
    )

def handle_job_repaired(event: JobStatusRepairedEvent):
    logistics_service = LogisticsService()
    logistics_service.create_pickup_request_for_repairer(
        job_id=event.job_id,
    )

def register_handlers():
    """Initialize and register logistics event handlers."""
    EventBus.subscribe(BidAcceptedEvent, handle_bid_accepted)
    EventBus.subscribe(JobStatusRepairedEvent, handle_job_repaired)
