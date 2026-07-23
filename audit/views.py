from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from audit.models import AuditLog

class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'audit/audit_logs.html'
    context_object_name = 'logs'
    paginate_by = 25
