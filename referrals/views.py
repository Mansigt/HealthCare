from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from referrals.models import Referral
from referrals.forms import ReferralForm, ReferralEditForm
from accounts.views import DoctorRequiredMixin, ClinicAdminRequiredMixin
from audit.signals import object_viewed
from clinics.models import Clinic

class ReferralListView(DoctorRequiredMixin, ListView):
    model = Referral
    template_name = 'referrals/referral_list.html'
    context_object_name = 'referrals'
    paginate_by = 10

    def get_queryset(self):
        return Referral.objects.filter(doctor=self.request.user)

class ReferralDetailView(LoginRequiredMixin, DetailView):
    model = Referral
    template_name = 'referrals/referral_detail.html'
    context_object_name = 'referral'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Check permissions
        is_doctor = (self.request.user.role == 'DOCTOR' and obj.doctor == self.request.user)
        is_clinic_admin = (self.request.user.role == 'CLINIC_ADMIN' and hasattr(self.request.user, 'managed_clinic') and obj.clinic == self.request.user.managed_clinic)
        
        if not (is_doctor or is_clinic_admin):
            raise Http404("Referral not found or access denied.")
            
        # Trigger audit log signal for viewing referral
        object_viewed.send(sender=Referral, instance=obj)
        return obj

class ReferralCreateView(DoctorRequiredMixin, CreateView):
    model = Referral
    form_class = ReferralForm
    template_name = 'referrals/referral_form.html'
    success_url = reverse_lazy('referral_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['doctor'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get('patient')
        clinic_id = self.request.GET.get('clinic')
        specialty_id = self.request.GET.get('specialty')
        
        if patient_id:
            initial['patient'] = patient_id
        if clinic_id:
            initial['clinic'] = clinic_id
        if specialty_id:
            initial['specialty'] = specialty_id
            
        return initial

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        form.instance.status = 'PENDING'
        messages.success(self.request, f"Referral created successfully for patient {form.instance.patient}.")
        return super().form_valid(form)

class ReferralUpdateView(DoctorRequiredMixin, UpdateView):
    model = Referral
    form_class = ReferralEditForm
    template_name = 'referrals/referral_form.html'
    success_url = reverse_lazy('referral_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['doctor'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.doctor != self.request.user:
            raise Http404("Referral not found.")
        if obj.status != 'PENDING':
            # Cannot edit if confirmed (i.e. Accepted, Rejected, Completed)
            messages.error(self.request, "Cannot edit this referral once it has been processed.")
            raise Http404("Referral editing is not available.")
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Referral updated successfully.")
        return super().form_valid(form)

class IncomingReferralListView(ClinicAdminRequiredMixin, ListView):
    model = Referral
    template_name = 'referrals/incoming_referrals.html'
    context_object_name = 'referrals'
    paginate_by = 10

    def get_queryset(self):
        try:
            clinic = self.request.user.managed_clinic
            return Referral.objects.filter(clinic=clinic)
        except Clinic.DoesNotExist:
            return Referral.objects.none()

class ProcessReferralView(ClinicAdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            clinic = request.user.managed_clinic
        except Clinic.DoesNotExist:
            messages.error(request, "Please register your clinic profile first.")
            return redirect('clinic_add')
            
        referral = get_object_or_404(Referral, pk=pk, clinic=clinic)
        action = request.POST.get('action')
        
        if action == 'accept':
            referral.status = 'ACCEPTED'
            messages.success(request, f"Referral for {referral.patient} has been Accepted.")
        elif action == 'reject':
            referral.status = 'REJECTED'
            messages.warning(request, f"Referral for {referral.patient} has been Rejected.")
        elif action == 'complete':
            referral.status = 'COMPLETED'
            messages.success(request, f"Referral for {referral.patient} has been Completed.")
        else:
            messages.error(request, "Invalid action.")
            
        referral.save()
        return redirect('incoming_referral_list')
