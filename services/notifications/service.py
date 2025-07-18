from .models import Notification


class NotificationService:
    def create_notification(self, user_id: int, title: str, message: str,
                            notification_type: str, notification_medium: str = 'ALL') -> Notification:
        return Notification.objects.create(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            notification_medium=notification_medium,
        )

    def mark_as_read(self, notification_id: int) -> Notification:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return notification

    def get_user_notifications(self, user_id: int, unread_only: bool = False):
        queryset = Notification.objects.filter(user_id=user_id)
        if unread_only:
            queryset = queryset.filter(is_read=False)
        return queryset.order_by('-created_at')
