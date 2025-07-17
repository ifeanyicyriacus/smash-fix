from common.event_bus import EventBus
from job.events import BidAcceptedEvent, RepairCompletedEvent

from services.payments.mocks import MockPaymentGateway, MockEscrowService
from services.payments.models import Escrow

escrow_service = MockEscrowService()
payment_gateway = MockPaymentGateway()


def handle_bid_accepted(event: BidAcceptedEvent):
    escrow_service.create_escrow(
        job_id=event.job_id,
        bid_amount=event.bid_amount
    )

def handle_repair_completed(event: RepairCompletedEvent):
    escrow = Escrow.objects.get(job_id=event.job_id)
    escrow_service.release_escrow(escrow)

def subscribe_to_events():
    EventBus.subscribe('BidAcceptedEvent', handle_bid_accepted)
    EventBus.subscribe('RepairCompletedEvent', handle_repair_completed)
