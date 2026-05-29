from django.conf import settings

from .permissions import (
    ALL_DASHBOARD_ROLES,
    ROLE_ADMIN,
    ROLE_FYSIO,
    ROLE_HEAD_PERFORMANCE,
    ROLE_PLAYER,
    ROLE_STRENGTH_TRAINER,
    ROLE_TEAM_TRAINER,
    has_dashboard_role,
)

FULL_STAFF_ROLES = {ROLE_ADMIN, ROLE_HEAD_PERFORMANCE, ROLE_FYSIO, ROLE_STRENGTH_TRAINER}
TEAM_DATA_ROLES = FULL_STAFF_ROLES | {ROLE_TEAM_TRAINER}


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
    user = request.user
    can_switch_app_mode = _can_switch_app_mode(request.user)
    requested_app_view = request.GET.get("app_view", "")
    player_preview_mode = can_switch_app_mode and requested_app_view == "player"
    player_app_mode = _is_player_app_user(request.user) or player_preview_mode
    can_full_staff = has_dashboard_role(user, FULL_STAFF_ROLES)
    can_team_data = has_dashboard_role(user, TEAM_DATA_ROLES)
    can_admin = has_dashboard_role(user, {ROLE_ADMIN})

    return {
        "APP_UI_ONLY_MODE": getattr(settings, "APP_UI_ONLY_MODE", False),
        "PLAYER_APP_MODE": player_app_mode,
        "PLAYER_APP_PREVIEW_MODE": player_preview_mode,
        "CAN_SWITCH_APP_MODE": can_switch_app_mode,
        "CURRENT_APP_VIEW": "player" if player_app_mode else "staff",
        "NAV_CAN_FULL_STAFF": can_full_staff,
        "NAV_CAN_TEAM_DATA": can_team_data,
        "NAV_CAN_ADMIN": can_admin,
    }
