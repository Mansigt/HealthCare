from django.db import models
from django.conf import settings

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Specialties"
        ordering = ['name']
        
    def __str__(self):
        return self.name

class InsuranceProvider(models.Model):
    provider_name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['provider_name']
        
    def __str__(self):
        return self.provider_name

class Clinic(models.Model):
    clinic_name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_number = models.CharField(max_length=20)
    estimated_wait_days = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'CLINIC_ADMIN'}, 
        related_name='managed_clinic'
    )
    specialties = models.ManyToManyField(Specialty, related_name='clinics', blank=True)
    insurance_providers = models.ManyToManyField(InsuranceProvider, related_name='clinics', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['clinic_name']

    def __str__(self):
        return self.clinic_name
