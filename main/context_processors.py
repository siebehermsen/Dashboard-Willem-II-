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


def _can_switch_app_mode(user):
    if not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return True
    staff_roles = ALL_DASHBOARD_ROLES - {ROLE_PLAYER}
    return user.groups.filter(name__in=staff_roles).exists()


def app_flags(request):
    can_switch_app_mode = _can_switch_app_mode(request.user)
    requested_app_view = request.GET.get("app_view", "")
    player_preview_mode = can_switch_app_mode and requested_app_view == "player"
    player_app_mode = _is_player_app_user(request.user) or player_preview_mode

    return {
        "APP_UI_ONLY_MODE": getattr(settings, "APP_UI_ONLY_MODE", False),
        "PLAYER_APP_MODE": player_app_mode,
        "PLAYER_APP_PREVIEW_MODE": player_preview_mode,
        "CAN_SWITCH_APP_MODE": can_switch_app_mode,
        "CURRENT_APP_VIEW": "player" if player_app_mode else "staff",
    }
