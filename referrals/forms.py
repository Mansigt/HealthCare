from django import forms
from referrals.models import Referral
from patients.models import Patient
from clinics.models import Clinic, Specialty

class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['patient', 'clinic', 'specialty', 'referral_notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'clinic': forms.Select(attrs={'class': 'form-select'}),
            'specialty': forms.Select(attrs={'class': 'form-select'}),
            'referral_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        if doctor:
            # Filter patients managed by this doctor
            self.fields['patient'].queryset = Patient.objects.filter(created_by=doctor)

class ReferralEditForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['patient', 'clinic', 'specialty', 'referral_notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'clinic': forms.Select(attrs={'class': 'form-select'}),
            'specialty': forms.Select(attrs={'class': 'form-select'}),
            'referral_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['patient'].queryset = Patient.objects.filter(created_by=doctor)

class ReferralStatusForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
