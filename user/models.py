from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

class Customer(User):
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)



class Repairer(User):
    FIELDS = (
    ("HW", "HARDWARE"),
    ("SW", "SOFTWARE")
    )
    nin = models.CharField(max_length=20)
    # skillset = models.JSONField()  # List of skills
    rating = models.FloatField(default=0.0)
    field = models.CharField(max_length=20, choices=FIELDS)
    wallet_id = models.CharField(max_length=50)
    verification_id = models.CharField(max_length=50)
    work_address = models.CharField(max_length=255)
