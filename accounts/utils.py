"""Helpers for accounts / user profiles."""
from django.contrib.auth.models import User

from .models import UserProfile


def ensure_user_profile(user: User) -> UserProfile:
    """
    Return the user's UserProfile, creating a sensible default if missing.

    New Django users (createsuperuser, shell, etc.) often have no profile yet;
    without this, session login and JWT login reject them.
    """
    try:
        return user.profile
    except UserProfile.DoesNotExist:
        pass

    base = f'EMP-{user.pk:06d}'
    emp_id = base
    suffix = 0
    while UserProfile.objects.filter(employee_id=emp_id).exists():
        suffix += 1
        emp_id = (base + f'-{suffix}')[:20]

    full = (user.get_full_name() or '').strip() or user.username
    role = 'Admin' if user.is_superuser else 'Physician'

    return UserProfile.objects.create(
        user=user,
        employee_id=emp_id,
        full_name=full[:150],
        role=role,
        designation=role,
        status='Active',
    )
