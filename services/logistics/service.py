from django.conf import settings

from services.logistics.mocks import MockLogisticsProvider, ClickNShipLogisticsProvider


class LogisticsService:
    def __init__(self):
        if settings.USE_SERVICE_MOCKS:
            self.provider = MockLogisticsProvider()
        else:
            self.provider = ClickNShipLogisticsProvider(
                username=settings.CLICKNSHIP_USERNAME,
                password=settings.CLICKNSHIP_PASSWORD
            )