"""Role-based access for session (template) views."""
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import UserProfile


def role_required(*allowed_roles):
    """
    Restrict a view to users whose profile.role is in allowed_roles.
    Admin may access any view that uses this decorator (same as API helpers).
    """
    allowed = set(allowed_roles) | {'Admin'}

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
            try:
                role = request.user.profile.role
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not configured.')
                return redirect(settings.LOGIN_URL)
            if role not in allowed:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
