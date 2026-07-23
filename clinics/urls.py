from django.urls import path
from clinics.views import (
    DoctorDashboardView, ClinicDashboardView, ClinicCreateView, 
    ClinicUpdateView, UpdateWaitTimeView, ClinicSearchListView, ClinicDetailView
)

urlpatterns = [
    path('dashboard/doctor/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('dashboard/clinic/', ClinicDashboardView.as_view(), name='clinic_dashboard'),
    path('add/', ClinicCreateView.as_view(), name='clinic_add'),
    path('edit/', ClinicUpdateView.as_view(), name='clinic_edit'),
    path('wait-time/update/', UpdateWaitTimeView.as_view(), name='clinic_wait_time_update'),
    path('search/', ClinicSearchListView.as_view(), name='clinic_search'),
    path('<int:pk>/', ClinicDetailView.as_view(), name='clinic_detail'),
]
