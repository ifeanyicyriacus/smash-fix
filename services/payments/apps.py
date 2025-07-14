from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services.payments'

    def ready(self):
        from . import event_handlers
        event_handlers.register_handlers()
