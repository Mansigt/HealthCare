from django.contrib import admin
from patients.models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'age', 'gender', 'phone', 'insurance_provider', 'created_by', 'created_at']
    list_filter = ['gender', 'insurance_provider', 'created_by']
    search_fields = ['first_name', 'last_name', 'phone', 'address']
    ordering = ['-created_at']

admin.site.register(Patient, PatientAdmin)
