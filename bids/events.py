
class BidCreatedEvent:
    def __init__(self, bid_id, repairer_id):
        self.bid_id = bid_id
        self.repairer_id = repairer_id

class BidStatusChangedEvent: #handles bid expiry...
    def __init__(self, bid_id, old_status, new_status):
        self.bid_id = bid_id
        self.old_status = old_status
        self.new_status = new_status