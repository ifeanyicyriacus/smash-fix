import uuid

from django.conf import settings
from django.db import models

from job.models import RepairJob


class Bid(models.Model):
    PART_QUALITY_CHOICES = [
        ('OEM', 'OEM'),
        ('3rdparty', '3rd Party'),
    ]

    BID_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name='bids')
    repairer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_of_repair = models.DurationField(help_text='Estimated repair duration')
    warranty = models.CharField(max_length=255, default='No warranty')
    message = models.TextField(blank=True, null=True)
    part_quality = models.CharField(max_length=10, choices=PART_QUALITY_CHOICES)
    status = models.CharField(max_length=10, choices=BID_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = getattr(self.repairer, 'username', 'Unknown')
        return f"Bid {self.id} by {self.repairer.username} on Job {self.job.id}"