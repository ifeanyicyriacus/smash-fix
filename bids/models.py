import uuid
from django.db import models
from django.conf import settings
from job.models import RepairJob
from user.models import Repairer

class Bid(models.Model):
    PART_QUALITY = (
        ('OEM', 'OEM'),
        ('3RDPARTY', '3RD_PARTY'),
    )
    BID_STATUS = (
        ('P', 'PENDING'),
        ('A', 'ACCEPTED'),
        ('R', 'REJECTED'),
        ('E', 'EXPIRED'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name='bids')
    repairer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'repairer': True})
    price = models.PositiveBigIntegerField()
    duration = models.DurationField(help_text="Estimated repair duration")  # Changed to DurationField
    part_quality = models.CharField(max_length=8, choices=PART_QUALITY, default='OEM')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=BID_STATUS, default='P')

    def __str__(self):
        return f"Bid {self.id} for Job {self.job.id} by {self.repairer.username}"
