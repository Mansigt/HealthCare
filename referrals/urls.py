from django.urls import path
from referrals.views import (
    ReferralListView, ReferralDetailView, ReferralCreateView, 
    ReferralUpdateView, IncomingReferralListView, ProcessReferralView
)

urlpatterns = [
    path('', ReferralListView.as_view(), name='referral_list'),
    path('create/', ReferralCreateView.as_view(), name='referral_create'),
    path('<int:pk>/', ReferralDetailView.as_view(), name='referral_detail'),
    path('<int:pk>/edit/', ReferralUpdateView.as_view(), name='referral_edit'),
    path('incoming/', IncomingReferralListView.as_view(), name='incoming_referral_list'),
    path('<int:pk>/process/', ProcessReferralView.as_view(), name='referral_process'),
]
