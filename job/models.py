from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

from user.models import Customer


class JOB_STATUS(models.TextChoices):
    OPEN = 'OPEN'
    BIDDING = 'BIDDING'
    ASSIGNED = 'ASSIGNED'
    IN_PROGRESS = 'IN_PROGRESS'
    REPAIRED = 'REPAIRED'
    CANCELLED = 'CANCELLED'

class RepairJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='repair_jobs')
    device_brand = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)
    issue_description = models.TextField()
    issue_image_video_links = ArrayField(models.URLField(), blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=JOB_STATUS.choices, default=JOB_STATUS.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
