import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings

class RepairJob(models.Model):
    JOB_STATUS = (
        ('OPEN', 'OPEN'),
        ('BIDDING', 'BIDDING'),
        ('ASSIGNED', 'ASSIGNED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('REPAIRED', 'REPAIRED'),
        ('CANCELLED', 'CANCELLED'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'customer': True})
    device_brand = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)
    issue_description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=JOB_STATUS, default='OPEN')
    image = models.ImageField(upload_to='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bid_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Job {self.id} - {self.device_brand} {self.device_model}"

class RepairJobImage(models.Model):
    issue_image_video_links = models.FileField(upload_to="phones/images_videos", blank=True, null=True)
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name="images_videos")

    def __str__(self):
        return f'{self.issue_image_video_links.url}'