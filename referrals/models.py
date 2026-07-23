from django.db import models
from django.conf import settings
from patients.models import Patient
from clinics.models import Clinic, Specialty

class Referral(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='referrals')
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'DOCTOR'}, 
        related_name='created_referrals'
    )
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='incoming_referrals')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='referrals')
    referral_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Referral: {self.patient} -> {self.clinic} ({self.get_status_display()})"
