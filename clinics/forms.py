from django import forms
from clinics.models import Clinic, Specialty, InsuranceProvider

class ClinicForm(forms.ModelForm):
    specialties = forms.ModelMultipleChoiceField(
        queryset=Specialty.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    insurance_providers = forms.ModelMultipleChoiceField(
        queryset=InsuranceProvider.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Clinic
        fields = [
            'clinic_name', 'address', 'city', 'latitude', 'longitude', 
            'contact_number', 'estimated_wait_days', 'description', 
            'specialties', 'insurance_providers'
        ]
        widgets = {
            'clinic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'estimated_wait_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class WaitTimeForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['estimated_wait_days']
        widgets = {
            'estimated_wait_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
