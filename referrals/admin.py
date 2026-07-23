from django.contrib.auth import get_user_model
from django.contrib import admin
from referrals.models import Referral

class ReferralAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'clinic', 'specialty', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'specialty', 'clinic', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__username', 'doctor__first_name', 'doctor__last_name', 'clinic__clinic_name']
    ordering = ['-created_at']

admin.site.register(Referral, ReferralAdmin)
