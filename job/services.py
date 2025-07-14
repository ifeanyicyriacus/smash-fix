

from common.event_bus import EventBus
from job.events import BidAcceptedEvent, JobStatusChangedEvent


class JobService:
    @staticmethod
    def accept_bid(job, bid):
        if job.status != 'bidding':
            raise ValueError('Job is not in bidding state')

        # State Transition
        old_status = job.status
        job.status = 'accepted'
        job.selected_bid = bid
        job.save()

        # Publish events
        events = [
            BidAcceptedEvent(
                job_id=job.id,
                repairer_id=bid.repairer_id,
                bid_amount=bid.price
            ),
            JobStatusChangedEvent(
                job_id=job.id,
                old_status=old_status,
                new_status=job.status
            )
        ]

        for event in events:
            EventBus.publish(event)
