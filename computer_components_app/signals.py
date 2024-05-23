from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserSession

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # Check if the user is in the "Manager" group
    is_manager = user.groups.filter(name='Manager').exists()
    # Create a UserSession entry
    UserSession.objects.create(
        user=user,
        session_key=request.session.session_key,
        login_time=timezone.now(),
        is_manager=is_manager
    )

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    # Update the logout_time for the UserSession entry
    UserSession.objects.filter(
        user=user,
        session_key=request.session.session_key,
        logout_time__isnull=True
    ).update(logout_time=timezone.now())