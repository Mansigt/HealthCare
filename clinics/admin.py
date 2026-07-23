from django.contrib import admin
from clinics.models import Specialty, InsuranceProvider, Clinic

class ClinicAdmin(admin.ModelAdmin):
    list_display = ['clinic_name', 'city', 'contact_number', 'estimated_wait_days', 'admin', 'created_at']
    list_filter = ['city', 'specialties', 'insurance_providers']
    search_fields = ['clinic_name', 'address', 'city', 'description']
    ordering = ['clinic_name']

admin.site.register(Specialty)
admin.site.register(InsuranceProvider)
admin.site.register(Clinic, ClinicAdmin)
