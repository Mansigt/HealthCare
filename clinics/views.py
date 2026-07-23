from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from clinics.models import Clinic, Specialty, InsuranceProvider
from clinics.forms import ClinicForm, WaitTimeForm
from clinics.ranking import get_ranked_clinics
from accounts.views import ClinicAdminRequiredMixin, DoctorRequiredMixin
from referrals.models import Referral
from patients.models import Patient

class DoctorDashboardView(DoctorRequiredMixin, TemplateView):
    template_name = 'clinics/doctor_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_referrals = Referral.objects.filter(doctor=self.request.user)
        context['total_referrals'] = my_referrals.count()
        context['pending_referrals'] = my_referrals.filter(status='PENDING').count()
        context['accepted_referrals'] = my_referrals.filter(status='ACCEPTED').count()
        context['completed_referrals'] = my_referrals.filter(status='COMPLETED').count()
        context['rejected_referrals'] = my_referrals.filter(status='REJECTED').count()
        
        # Patients statistics
        context['total_patients'] = Patient.objects.filter(created_by=self.request.user).count()
        context['recent_patients'] = Patient.objects.filter(created_by=self.request.user).order_by('-created_at')[:5]
        
        # Recent referrals
        context['recent_referrals'] = my_referrals.order_by('-created_at')[:5]
        
        # Global statistics
        context['total_clinics'] = Clinic.objects.count()
        
        # Fetch wait times for statistics chart
        all_clinics = Clinic.objects.all().order_by('estimated_wait_days')[:10]
        context['wait_time_labels'] = [c.clinic_name for c in all_clinics]
        context['wait_time_values'] = [c.estimated_wait_days for c in all_clinics]

        return context

class ClinicDashboardView(ClinicAdminRequiredMixin, TemplateView):
    template_name = 'clinics/clinic_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            clinic = self.request.user.managed_clinic
            context['clinic'] = clinic
            incoming = Referral.objects.filter(clinic=clinic)
            context['total_incoming'] = incoming.count()
            context['pending_incoming'] = incoming.filter(status='PENDING').count()
            context['accepted_incoming'] = incoming.filter(status='ACCEPTED').count()
            context['completed_incoming'] = incoming.filter(status='COMPLETED').count()
            context['rejected_incoming'] = incoming.filter(status='REJECTED').count()
            context['recent_incoming'] = incoming.order_by('-created_at')[:5]
            context['wait_time_form'] = WaitTimeForm(instance=clinic)
            
            # Chart data for clinic administrator
            context['incoming_status_labels'] = ['Pending', 'Accepted', 'Rejected', 'Completed']
            context['incoming_status_data'] = [
                incoming.filter(status='PENDING').count(),
                incoming.filter(status='ACCEPTED').count(),
                incoming.filter(status='REJECTED').count(),
                incoming.filter(status='COMPLETED').count(),
            ]
        except Clinic.DoesNotExist:
            context['clinic'] = None
            
        return context

class ClinicCreateView(ClinicAdminRequiredMixin, CreateView):
    model = Clinic
    form_class = ClinicForm
    template_name = 'clinics/clinic_form.html'
    success_url = reverse_lazy('clinic_dashboard')

    def form_valid(self, form):
        if Clinic.objects.filter(admin=self.request.user).exists():
            messages.error(self.request, "You already manage a clinic.")
            return redirect('clinic_dashboard')
        form.instance.admin = self.request.user
        messages.success(self.request, "Clinic profile created successfully.")
        return super().form_valid(form)

class ClinicUpdateView(ClinicAdminRequiredMixin, UpdateView):
    model = Clinic
    form_class = ClinicForm
    template_name = 'clinics/clinic_form.html'
    success_url = reverse_lazy('clinic_dashboard')

    def get_object(self, queryset=None):
        try:
            return self.request.user.managed_clinic
        except Clinic.DoesNotExist:
            raise Http404("You don't have a clinic profile yet.")

    def form_valid(self, form):
        messages.success(self.request, "Clinic information updated successfully.")
        return super().form_valid(form)

class UpdateWaitTimeView(ClinicAdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        clinic = get_object_or_904(Clinic, admin=request.user)
        form = WaitTimeForm(request.POST, instance=clinic)
        if form.is_valid():
            form.save()
            messages.success(request, f"Wait time updated to {clinic.estimated_wait_days} days.")
        else:
            messages.error(request, "Failed to update wait time. Invalid value.")
        return redirect('clinic_dashboard')

class ClinicSearchListView(DoctorRequiredMixin, ListView):
    model = Clinic
    template_name = 'clinics/clinic_list.html'
    context_object_name = 'clinics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['insurances'] = InsuranceProvider.objects.all()
        
        # Pass search attributes to maintain form values in view
        context['selected_specialty'] = self.request.GET.get('specialty', '')
        context['selected_insurance'] = self.request.GET.get('insurance', '')
        context['selected_city'] = self.request.GET.get('city', '')
        context['doctor_lat'] = self.request.GET.get('lat', '')
        context['doctor_lng'] = self.request.GET.get('lng', '')
        
        # If doctor coordinates are not available, flag it
        context['has_location'] = bool(context['doctor_lat'] and context['doctor_lng'])
        return context

    def get_queryset(self):
        specialty_id = self.request.GET.get('specialty')
        insurance_provider_id = self.request.GET.get('insurance')
        city = self.request.GET.get('city')
        lat = self.request.GET.get('lat')
        lng = self.request.GET.get('lng')

        doctor_lat = float(lat) if lat else None
        doctor_lng = float(lng) if lng else None

        queryset = Clinic.objects.all()
        return get_ranked_clinics(
            clinics_queryset=queryset,
            specialty_id=specialty_id,
            insurance_provider_id=insurance_provider_id,
            city=city,
            doctor_lat=doctor_lat,
            doctor_lng=doctor_lng
        )

class ClinicDetailView(LoginRequiredMixin, DetailView):
    model = Clinic
    template_name = 'clinics/clinic_detail.html'
    context_object_name = 'clinic'
