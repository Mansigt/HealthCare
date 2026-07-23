from django.contrib import admin
from audit.models import AuditLog

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'username', 'action', 'model_name', 'object_id', 'ip_address']
    list_filter = ['action', 'model_name']
    search_fields = ['username', 'action', 'model_name', 'object_id', 'ip_address']
    ordering = ['-timestamp']
    
    # Audit logs should not be editable via admin panel
    readonly_fields = ['user', 'username', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(AuditLog, AuditLogAdmin)
