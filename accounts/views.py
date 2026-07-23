from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, TemplateView
from django.contrib import messages
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, LoginForm, UserProfileForm

class DoctorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'DOCTOR'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Access denied. Only doctors can access this page.")
            return redirect('dashboard')
        return super().handle_no_permission()

class ClinicAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'CLINIC_ADMIN'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Access denied. Only Clinic Administrators can access this page.")
            return redirect('dashboard')
        return super().handle_no_permission()

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Account created successfully for {user.username}! Please log in.")
        return super().form_valid(form)

class CustomLoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect('home')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

class DashboardRouterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'DOCTOR':
            return redirect('doctor_dashboard')
        elif request.user.role == 'CLINIC_ADMIN':
            return redirect('clinic_dashboard')
        else:
            messages.warning(request, "No dashboard configured for your role.")
            return redirect('home')
