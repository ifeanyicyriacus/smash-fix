from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_CLASS = (
        ('SYSTEM', 'System'),
        ('JOB', 'Job'),
        ('BID', 'Bid'),
        ('RATING', 'Rating'),
        ('LOGISTICS', 'Logistics'),
    )

    NOTIFICATION_TYPES = (
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('BOTH', 'Both'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_class = models.CharField(
        max_length=10,
        choices=NOTIFICATION_CLASS,
        default='NOTIFICATION'
    )
    notification_type = models.CharField(
        max_length=5,
        choices=NOTIFICATION_TYPES,
        default='EMAIL'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(null=True, blank=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username} - {self.title} - {self.notification_class}"

