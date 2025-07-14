from abc import ABC, abstractmethod
from typing import Dict, List, Any


class NotificationInterface(ABC):
    """Interface defining the contract for notification services.

    This interface specifies the required methods that any notification
    service implementation must provide to handle different types of
    notifications including email, SMS, and push notifications.
    """

    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str, attachments: List[Any] = None) -> bool:
        """Send an email notification.

        Args:
            recipient: Email address of the recipient
            subject: Subject line of the email
            body: Main content of the email
            attachments: Optional list of files to attach

        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass

    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send an SMS notification.

        Args:
            phone_number: Recipient's phone number
            message: Text message content

        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass

    @abstractmethod
    def send_push_notification(self, user_id: str, title: str, message: str, data: Dict[str, Any] = None) -> bool:
        """Send a push notification.

        Args:
            user_id: ID of the recipient user
            title: Title of the notification
            message: Main notification message
            data: Optional additional data payload

        Returns:
            bool: True if sent successfully, False otherwise
        """
        pass

    @abstractmethod
    def send_batch_notifications(self, notifications: List[Dict[str, Any]]) -> Dict[str, List[bool]]:
        """Send multiple notifications in batch.

        Args:
            notifications: List of notification configurations containing
                         type and required parameters for each notification

        Returns:
            Dict[str, List[bool]]: Results mapped by notification type
        """
        pass
