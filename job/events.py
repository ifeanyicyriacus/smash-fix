
class JobCreatedEvent:
    def __init__(self, job_id, customer_id):
        self.job_id = job_id
        self.customer_id = customer_id

class BidAcceptedEvent:
    def __init__(self, job_id, repairer_id, bid_amount):
        self.job_id = job_id
        self.repairer_id = repairer_id
        self.bid_amount = bid_amount

class JobStatusChangedEvent: #handles job expiry...
    def __init__(self, job_id, old_status, new_status):
        self.job_id = job_id
        self.old_status = old_status
        self.new_status = new_status
