from django.urls import path
from patients.views import PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView

urlpatterns = [
    path('', PatientListView.as_view(), name='patient_list'),
    path('add/', PatientCreateView.as_view(), name='patient_add'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='patient_edit'),
]
