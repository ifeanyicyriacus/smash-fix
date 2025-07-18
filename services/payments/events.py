from common.events import BaseEvent


class EscrowCreatedEvent(BaseEvent):
    event_name = "escrow_created"

    def __init__(self, escrow_id: str, job_id: str, **kwargs):
        super().__init__(**kwargs)
        self.escrow_id = escrow_id
        self.job_id = job_id

