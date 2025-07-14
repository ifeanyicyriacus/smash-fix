class EventBus:
    _subscribers = {}

    @classmethod
    def subscribe(cls, event_type, handler):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(handler)

    @classmethod
    def publish(cls, event):
        if event.type in cls._subscribers:
            for handler in cls._subscribers[event.type]:
                handler(event)

class InMemoryEventBus(EventBus):
    pass

class RedisEventBus(EventBus):
    pass