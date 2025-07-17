from django.db import models

LOGISTICS_STATUS = [
    ('PENDING', 'Pending'),
    ('ASSIGNED', 'Assigned'),
    ('PICKED_UP', 'Picked Up'),
    ('IN_TRANSIT', 'In Transit'),
    ('DELIVERED', 'Delivered'),
    ('FAILED', 'Failed'),
]

class LogisticsAssignment(models.Model):
    job_id = models.CharField(max_length=36)  # UUID from external system
    courier_id = models.CharField(max_length=255, null=True, blank=True)
    waybill_number = models.CharField(max_length=255, null=True, blank=True)
    pick_up_address = models.CharField(max_length=255, null=True, blank=True)
    drop_off_address = models.CharField(max_length=255, null=True, blank=True)
    tracking_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=LOGISTICS_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)