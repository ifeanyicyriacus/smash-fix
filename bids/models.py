from django.db import models

class BidStatus(models.Model):
    bid_status = (
    ('P', 'PENDING'),
    ('A', 'ACCEPTED'),
    ('R', 'REJECTED'),
    ('E','EXPIRED')
    )



class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    repairer_id = models.Foreignkey(Repairer)
    price = models.PositiveBigIntegerField()
    duration = models.DateTimeField()
    part_quality =
    created_at = models.DateTimeField(auto_add=True)
    status = models.CharField(max_length=1, choices=bid_status, default="P")
