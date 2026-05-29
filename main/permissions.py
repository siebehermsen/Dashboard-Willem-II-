from functools import wraps

from django.core.exceptions import PermissionDenied


ROLE_ADMIN = "Dashboard Admin"
ROLE_HEAD_PERFORMANCE = "Head of Performance"
ROLE_FYSIO = "Fysio"
ROLE_STRENGTH_TRAINER = "Krachttrainer"
ROLE_TEAM_TRAINER = "Teamtrainer"
ROLE_PERFORMANCE = ROLE_HEAD_PERFORMANCE
ROLE_MEDICAL = ROLE_FYSIO
ROLE_TRAINER = ROLE_TEAM_TRAINER
ROLE_READ_ONLY = "Alleen lezen"
ROLE_PLAYER = "Speler"

ROLE_CHOICES = (
    (ROLE_ADMIN, "Admin"),
    (ROLE_HEAD_PERFORMANCE, "Head of Performance"),
    (ROLE_FYSIO, "Fysio"),
    (ROLE_STRENGTH_TRAINER, "Krachttrainer"),
    (ROLE_TEAM_TRAINER, "Teamtrainer"),
    (ROLE_READ_ONLY, "Alleen lezen"),
    (ROLE_PLAYER, "Speler"),
)

ALL_DASHBOARD_ROLES = {role for role, _label in ROLE_CHOICES} | {ROLE_PLAYER}

LEGACY_ROLE_ALIASES = {
    ROLE_HEAD_PERFORMANCE: {"Performance Staff"},
    ROLE_FYSIO: {"Medisch"},
    ROLE_TEAM_TRAINER: {"Trainer"},
}


def has_dashboard_role(user, allowed_roles):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    group_names = set(allowed_roles)
    for role in allowed_roles:
        group_names.update(LEGACY_ROLE_ALIASES.get(role, set()))
    return user.groups.filter(name__in=group_names).exists()


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
