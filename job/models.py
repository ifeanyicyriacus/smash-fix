import uuid
from typing import TYPE_CHECKING

from django.db import models
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField

class RepairJob(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('bidding', 'Bidding'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    device_brand = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)
    issue_description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    image = CloudinaryField('media', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bid_deadline = models.DateTimeField(default=timezone.now)
    # blend it in later
    selected_bid = models.ForeignKey('bids.Bid', on_delete=models.SET_NULL, null=True, related_name='job')

    def save(self, *args, **kwargs):
        if not self.bid_deadline:
            self.bid_deadline = timezone.now() + timezone.timedelta(hours=48)
        super().save(*args, **kwargs)

    def __str__(self):
        username = getattr(self.customer, 'username', 'Unknown')
        return f"Job {self.id} ({self.device_brand} {self.device_model}) by {username}"
