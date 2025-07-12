from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('repairer', 'Repairer'),
        ('customer', 'Customer'),
        ('both', 'Both'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Customer(User):
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Repairer(User):
    FIELD_CHOICES = (
        ('hardware', 'Hardware'),
        ('software', 'Software'),
    )
    nin = models.CharField(max_length=20, unique=True)
    rating = models.FloatField(default=0.0, editable=False)
    field = models.CharField(max_length=20, choices=FIELD_CHOICES)
    wallet_id = models.CharField(max_length=50, unique=True)
    verification_id = models.CharField(max_length=50, unique=True)
    work_address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Repairer"
        verbose_name_plural = "Repairers"
