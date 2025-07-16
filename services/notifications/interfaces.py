from abc import ABC, abstractmethod
from services.notifications.models import Notification


class NotificationInterface(ABC):
    @abstractmethod
    def send_notification(self, notification: Notification) -> bool:
        """Send a single notification using the appropriate channel based on the notification type.

        Args:
            notification: Notification object containing recipient, content and delivery preferences

        Returns:
            bool: True if notification was sent successfully, False otherwise
        """
        pass
