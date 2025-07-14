from common.events import BaseEvent

class BidCreatedEvent(BaseEvent):
    event_name = "bid_created"
    def __init__(self, bid_id, repairer_id, **kwargs):
        super().__init__(**kwargs)
        self.bid_id = bid_id
        self.repairer_id = repairer_id

class BidStatusChangedEvent(BaseEvent): #handles bid expiry...
    event_name = "bid_status_changed"
    def __init__(self, bid_id, old_status, new_status, **kwargs):
        super().__init__(**kwargs)
        self.bid_id = bid_id
        self.old_status = old_status
        self.new_status = new_status