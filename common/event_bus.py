from typing import List, Callable, Dict
from .events import BaseEvent

class EventBus:
    _subscribers:Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_type:str, handler:Callable):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(handler)

    @classmethod
    def publish(cls, event:BaseEvent):
        if event.type in cls._subscribers:
            for handler in cls._subscribers[event.type]:
                handler(event)

class InMemoryEventBus(EventBus):
    pass

class RedisEventBus(EventBus):
    pass


# def subscribe(param):
#     return None
def event_bus():
    return None