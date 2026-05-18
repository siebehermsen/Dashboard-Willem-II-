from functools import wraps

from django.core.exceptions import PermissionDenied


ROLE_ADMIN = "Dashboard Admin"
ROLE_PERFORMANCE = "Performance Staff"
ROLE_MEDICAL = "Medisch"
ROLE_TRAINER = "Trainer"
ROLE_READ_ONLY = "Alleen lezen"

ROLE_CHOICES = (
    (ROLE_ADMIN, "Admin"),
    (ROLE_PERFORMANCE, "Performance staff"),
    (ROLE_MEDICAL, "Medisch"),
    (ROLE_TRAINER, "Trainer"),
    (ROLE_READ_ONLY, "Alleen lezen"),
)

ALL_DASHBOARD_ROLES = {role for role, _label in ROLE_CHOICES}


def has_dashboard_role(user, allowed_roles):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=allowed_roles).exists()


def role_required(*roles, allow_read_only_get=False):
    allowed_roles = set(roles)
    if allow_read_only_get:
        allowed_roles.add(ROLE_READ_ONLY)

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.method not in ("GET", "HEAD", "OPTIONS") and request.user.groups.filter(name=ROLE_READ_ONLY).exists():
                raise PermissionDenied
            if has_dashboard_role(request.user, allowed_roles):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied

        return wrapped

    return decorator
