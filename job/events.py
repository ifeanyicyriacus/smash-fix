from common.events import BaseEvent


class JobCreatedEvent:
    def __init__(self, job_id, customer_id):
        self.job_id = job_id
        self.customer_id = customer_id


# very important
class BidAcceptedEvent(BaseEvent):
    event_name = "bid_accepted"

    def __init__(self, job_id, repairer_id, bid_amount, **kwargs):
        super().__init__(**kwargs)
        self.job_id = job_id
        self.repairer_id = repairer_id
        self.bid_amount = bid_amount


class JobStatusRepairedEvent(BaseEvent):
    event_name = "job_repaired"

    def __init__(self, job_id, repair_details, **kwargs):
        super().__init__(**kwargs)
        self.job_id = job_id
        self.repair_details = repair_details

# class JobStatusChangedEvent(BaseEvent):  #handles job expiry...
#     event_name = "job_status_changed"
#
#     def __init__(self, job_id, old_status, new_status, **kwargs):
#         super().__init__(**kwargs)
#         self.job_id = job_id
#         self.old_status = old_status
#         self.new_status = new_status
