from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('DOCTOR', 'Doctor'),
        ('CLINIC_ADMIN', 'Clinic Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='DOCTOR')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
