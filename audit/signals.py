from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal
from referrals.models import Referral
from patients.models import Patient
from audit.models import AuditLog
from audit.middleware import get_current_request, get_ip_from_request

# Custom signal for viewing objects
object_viewed = Signal()

def create_audit_log(user, action, model_name, object_id, ip_address=None):
    request = get_current_request()
    
    # Resolve user
    if not user or user.is_anonymous:
        if request and request.user and request.user.is_authenticated:
            user = request.user
        else:
            user = None
            
    username = user.username if user else "System"
    
    # Resolve IP address
    if not ip_address:
        if request:
            ip_address = get_ip_from_request(request)
        else:
            ip_address = "127.0.0.1"

    AuditLog.objects.create(
        user=user,
        username=username,
        action=action,
        model_name=model_name,
        object_id=str(object_id) if object_id else None,
        ip_address=ip_address
    )

@receiver(post_save, sender=Referral)
def referral_post_save(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    create_audit_log(
        user=None,
        action=action,
        model_name="Referral",
        object_id=instance.id
    )

@receiver(post_delete, sender=Referral)
def referral_post_delete(sender, instance, **kwargs):
    create_audit_log(
        user=None,
        action="Deleted",
        model_name="Referral",
        object_id=instance.id
    )

@receiver(post_save, sender=Patient)
def patient_post_save(sender, instance, created, **kwargs):
    # Create audit log only if updated, as per requirement: "Patient updated"
    if not created:
        create_audit_log(
            user=None,
            action="Updated",
            model_name="Patient",
            object_id=instance.id
        )

@receiver(object_viewed)
def handle_object_viewed(sender, instance, **kwargs):
    model_name = instance.__class__.__name__
    create_audit_log(
        user=None,
        action="Viewed",
        model_name=model_name,
        object_id=instance.id
    )
