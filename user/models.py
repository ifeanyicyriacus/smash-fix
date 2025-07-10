from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

class Customer(User):
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)

class Repairer(User):
    nin = models.CharField(max_length=20)
    skill_set = models.JSONField()
    rating = models.FloatField(default=0.0)
    field = models.CharField(max_length=50)
    wallet_id = models.CharField(max_length=50)
    verification_id = models.CharField(max_length=50)
    work_address = models.CharField(max_length=255)
