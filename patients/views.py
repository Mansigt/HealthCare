from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from patients.models import Patient
from patients.forms import PatientForm
from accounts.views import DoctorRequiredMixin
from audit.signals import object_viewed

class PatientListView(DoctorRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

class PatientDetailView(DoctorRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Patient not found or access denied.")
        # Trigger audit log signal for viewing patient
        object_viewed.send(sender=Patient, instance=obj)
        return obj

class PatientCreateView(DoctorRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Patient {form.instance.full_name} added successfully.")
        return super().form_valid(form)

class PatientUpdateView(DoctorRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise Http404("Patient not found or access denied.")
        return obj

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance.full_name} updated successfully.")
        return super().form_valid(form)
