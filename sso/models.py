from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    TIER = [
        ("T5", "SuspendedUser"),
        ("T4", "User"),
        ("T3", "StarUser"),
        ("T2", "Admin"),
        ("T1", "SuperAdmin"),
    ]
    status = models.CharField(max_length=2, choices=TIER, default="T4")
