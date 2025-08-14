from typing import List, Dict, Any

from services.notifications.interfaces import NotificationInterface
from services.notifications.models import Notification




class MockNotificationService(NotificationInterface):
    @classmethod
    def _send_sms(cls, phone_number: str, title:str, message: str) -> bool:
        # Mock successful SMS sending
        return True

    @classmethod
    def _send_email(cls, recipient_email: str, subject: str, body: str) -> bool:
        # Mock successful email sending
        return True

    @classmethod
    def _send_push_notification(cls, user_id: str, title: str, message: str) -> bool:
        # Mock successful push notification sending
        return True

    def __init__(self):
        self.sms_enabled = True
        self.email_enabled = True
        self.push_enabled = True

    def send_notification(self, notification:Notification) -> bool:
        """Send notification based on type using mock services."""
        success = True
        if notification.notification_type == "SMS" and self.sms_enabled:
            success &= self._send_sms(
                notification.user.phone,
                notification.title,
                notification.message
            )

        if notification.notification_type == "EMAIL" and self.email_enabled:
            success &= self._send_email(
                notification.user.email,
                notification.title,
                notification.message
            )

        if notification.notification_type == "PUSH" and self.push_enabled:
            success &= self._send_push_notification(
                str(notification.user.id),
                notification.title,
                notification.message
            )

        return success
