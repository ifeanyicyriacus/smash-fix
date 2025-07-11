from django.db import models
import uuid

from job.models import RepairJob
from user.models import Repairer


class BidStatus(models.TextChoices):
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'
    EXPIRED = 'E'

class Bid(models.Model):
    PART_QUALITY = (
        ('OEM', 'OEM'),
        ('3RDPARTY', '3RD_PARTY')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name='bids')
    repairer = models.ForeignKey(Repairer, on_delete=models.CASCADE, related_name='bids')
    price = models.PositiveBigIntegerField()
    duration = models.DateTimeField()
    part_quality = models.CharField(max_length=8, choices=PART_QUALITY, default="OEM")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=BidStatus.choices, default=BidStatus.PENDING)
