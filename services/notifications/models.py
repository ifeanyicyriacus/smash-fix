from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('SYSTEM', 'System'),
        ('JOB_UPDATE', 'Job Update'),
        ('BID_UPDATE', 'Bid Update'),
        ('RATING', 'Rating'),
        ('LOGISTICS', 'Logistics'),
    )

    NOTIFICATION_MEDIUM = (
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push'),
        ('BOTH', 'Both'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='SYSTEM'
    )
    notification_medium = models.CharField(
        max_length=10,
        choices=NOTIFICATION_MEDIUM,
        default='EMAIL'
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.notification_type}"
