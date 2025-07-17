from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services.payments'

    def ready(self):
        from . import event_handlers
        event_handlers.subscribe_to_events()

        from .event_handlers import handle_bid_accepted, handle_repair_completed
        from common.event_bus import event_bus
        from job.events import BidAcceptedEvent, RepairCompletedEvent

        event_bus.subscribe(BidAcceptedEvent, handle_bid_accepted)
        event_bus.subscribe(RepairCompletedEvent, handle_repair_completed)