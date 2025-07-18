class JobCreatedEvent:
    def __init__(self, job_id, customer_id):
        self.job_id = job_id
        self.customer_id = customer_id

class JobStatusChangedEvent:
    def __init__(self, job_id, old_status, new_status, **kwargs):
        self.job_id = job_id
        self.old_status = old_status
        self.new_status = new_status


class BidAcceptedEvent:
    def __init__(self, job_id, bid_id, repairer_id, bid_amount, customer_id):
        self.job_id = job_id
        self.bid_id = bid_id
        self.repairer_id = repairer_id
        self.customer_id = customer_id
        self.bid_amount = bid_amount

class JobStatusRepairedEvent:
    def __init__(self, job_id, **kwargs):
        self.job_id = job_id

class RepairCompletedEvent:
    def __init__(self, job_id, repairer_id, **kwargs):
        self.job_id = job_id
        self.repairer_id = repairer_id
