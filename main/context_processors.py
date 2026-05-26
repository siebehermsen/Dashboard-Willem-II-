from django.conf import settings

from .permissions import ROLE_PLAYER, ALL_DASHBOARD_ROLES


def _is_player_app_user(user):
    if not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return False
    if not user.groups.filter(name=ROLE_PLAYER).exists():
        return False
    return not user.groups.filter(name__in=ALL_DASHBOARD_ROLES - {ROLE_PLAYER}).exists()


def app_flags(request):
    return {
        "APP_UI_ONLY_MODE": getattr(settings, "APP_UI_ONLY_MODE", False),
        "PLAYER_APP_MODE": _is_player_app_user(request.user),
    }
