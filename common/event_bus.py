from typing import Type, Callable, Any


class EventBus:
    _subscribers = {}

    @classmethod
    def subscribe(cls, event_type: Type):
        def decorator(handler: Callable):
            if event_type not in cls._subscribers:
                cls._subscribers[event_type] = []
            cls._subscribers[event_type].append(handler)
            return handler

        return decorator

    @classmethod
    def publish(cls, event: Any):
        event_type = type(event)
        if event_type in cls._subscribers:
            for handler in cls._subscribers[event_type]:
                handler(event)


# Singleton instance
event_bus = EventBus()