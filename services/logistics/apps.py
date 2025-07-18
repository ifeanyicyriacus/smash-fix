from django.apps import AppConfig


class LogisticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services.logistics'

    def ready(self):
        from .event_handlers import handle_bid_accepted
        from common.event_bus import event_bus
        from job.events import BidAcceptedEvent

        event_bus.subscribe(BidAcceptedEvent, handle_bid_accepted)
