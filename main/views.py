from django.http import HttpResponse
import csv
from .models import Player, DayProgramEntry, Oefening
from django.db.models import Avg, Sum
from django.http import JsonResponse
from .models import Player, WellnessEntry
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import (
    Player,
    OverigNote,
    BeleidSectionImage,
    Staff,
    BirthdayRecord,
    BirthdayProfile,
    YouthGuestWeek,
    YouthGuestProfile,
    VakantieProgrammaEntry,
    VakantiePlanning,
    GrowthProfile,
    GrowthMeasurement,
)
from django.db.models import Avg, Min, Max
from django.utils import timezone
from .models import Match, Team

# ---------- IMPORTS ----------
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Avg, Q
from django import forms
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta
from types import SimpleNamespace
from django.conf import settings
from django.urls import reverse
from django.core.files.storage import default_storage
from django.views.decorators.cache import never_cache
import os
import uuid
import shutil
import subprocess
from urllib.parse import parse_qs, urlparse
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None
from django.utils.dateparse import parse_date
from .models import (
    InjuryCase,
    InjuryType,
    InjuryPhase,
    InjuryStatus,
    RPEEntry,
    RPETrainingType,
    PlayerSpeedTest,
    HitWeekPlan,
    HitWeekPlanEntry,
    BeweeganalysePunt,
    BeweeganalyseSessie,
    BeweeganalyseBeoordeling,
    PerformanceMetricType,
    PerformanceSession,
    PerformanceSessionKind,
    PlayerTeamAssignment,
    PlayerMonitoringProfile,
    PlayerPosition,
    StaffRole,
    AuditLog,
    DataImportLog,
)
from .permissions import ALL_DASHBOARD_ROLES, LEGACY_ROLE_ALIASES, ROLE_CHOICES, ROLE_ADMIN, ROLE_PLAYER, role_required
from .performance_3nf import fetch_performance_rows, mean, upsert_performance_session_metrics


def _dashboard_role_values():
    values = {role for role, _label in ROLE_CHOICES}
    for aliases in LEGACY_ROLE_ALIASES.values():
        values.update(aliases)
    return values


def _dashboard_role_label(role_name):
    return dict(ROLE_CHOICES).get(role_name, "")


def _user_dashboard_role(user):
    if not user:
        return ""
    role_values = _dashboard_role_values()
    legacy_to_current = {
        legacy: current
        for current, aliases in LEGACY_ROLE_ALIASES.items()
        for legacy in aliases
    }
    for group in user.groups.all():
        if group.name in legacy_to_current:
            return legacy_to_current[group.name]
        if group.name in role_values:
            return group.name
    return ""


def _sync_user_dashboard_role(user, dashboard_role):
    role_values = _dashboard_role_values()
    user.groups.remove(*Group.objects.filter(name__in=role_values))
    if dashboard_role:
        group, _ = Group.objects.get_or_create(name=dashboard_role)
        user.groups.add(group)
    user.is_staff = dashboard_role == ROLE_ADMIN or user.is_superuser
    user.save()


def _is_player_app_user(user):
    if not getattr(user, "is_authenticated", False) or user.is_superuser:
        return False
    if not user.groups.filter(name=ROLE_PLAYER).exists():
        return False
    staff_roles = ALL_DASHBOARD_ROLES - {ROLE_PLAYER}
    return not user.groups.filter(name__in=staff_roles).exists()


def _player_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return None
    player = getattr(user, "player_profile", None)
    if player:
        return player
    username = (user.get_username() or "").strip()
    if not username:
        return None
    normalized_username = username.replace(".", " ").replace("_", " ").replace("-", " ").strip()
    return Player.objects.filter(Q(name__iexact=username) | Q(name__iexact=normalized_username)).first()


def _require_own_player_for_player_user(request, player_id):
    if not _is_player_app_user(request.user):
        return
    player = _player_for_user(request.user)
    if not player or str(player.id) != str(player_id):
        raise PermissionDenied


def _record_audit(request, *, action, category, object_label="", details=""):
    user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
    AuditLog.objects.create(
        actor=user,
        action=action,
        category=category,
        object_label=object_label or "",
        details=details or "",
    )


def _is_admin_user(user):
    return bool(
        getattr(user, "is_authenticated", False)
        and (getattr(user, "is_superuser", False) or _user_dashboard_role(user) == ROLE_ADMIN)
    )


def logout_view(request):
    logout(request)
    return redirect("login")


@never_cache
def service_worker(request):
    response = render(request, "sw.js", content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


def offline_page(request):
    return render(request, "offline.html", status=200)



# ---------- INLINE FORM (GEEN forms.py NODIG) ----------
class WeekProgramForm(forms.ModelForm):
    class Meta:
        model = DayProgramEntry
        fields = [
            "date",
            "team",
            "category",
            "context",
            "location",
            "start_time",
            "end_time",
            "responsible",
            "physical_note",
            "activities",
            "notes",
        ]


def _resolve_player_by_name(name):
    if not name:
        return None
    return Player.objects.filter(name=name).first()


def _get_or_create_monitoring_profile(player):
    profile, _ = PlayerMonitoringProfile.objects.get_or_create(player=player)
    return profile


def _injury_duration_days(injury):
    if injury.started_on and injury.expected_return_on:
        return (injury.expected_return_on - injury.started_on).days
    return None


def _injury_to_ui(injury):
    phase_code = injury.phase_ref.code if injury.phase_ref else ""
    phase_label_map = {
        "early": "Vroege fase",
        "mid": "Middenfase",
        "final": "Laatste fase",
    }
    return SimpleNamespace(
        id=injury.id,
        name=injury.player.name if injury.player else "",
        injury_type=injury.injury_type_ref.name if injury.injury_type_ref else "-",
        start_date=injury.started_on,
        expected_return=injury.expected_return_on,
        duration=_injury_duration_days(injury),
        phase=phase_code,
        phase_label=phase_label_map.get(phase_code, "Laatste fase"),
        status=injury.status_ref.code if injury.status_ref else "",
    )


def _agenda_category_label(category):
    labels = {
        "training": "Training",
        "kracht": "Krachttraining",
        "testing": "Testing",
        "data": "Data",
        "wedstrijd": "Wedstrijd",
        "toernooi": "Toernooi",
        "rust": "Rustdag",
        "overig": "Overig",
    }
    return labels.get((category or "").strip().lower(), category or "Training")


def _attendance_status_from_agenda(chosen_date, team_code):
    team_code = (team_code or "").strip().upper()
    if not team_code:
        return None, None

    agenda_entry = (
        DayProgramEntry.objects
        .filter(date=chosen_date, team__iexact=team_code)
        .exclude(category__iexact="rust")
        .order_by("start_time", "id")
        .first()
    )
    if not agenda_entry:
        return None, None

    category = (agenda_entry.category or "training").strip().lower()
    if category == "wedstrijd":
        base_code = "wedstrijd"
        base_label = "Wedstrijd"
    else:
        base_code = "training"
        base_label = "Training"

    status_code = f"{base_code}_{team_code.lower()}"
    status, _created = AttendanceStatus.objects.get_or_create(
        code=status_code,
        defaults={
            "label": f"{base_label} {team_code}",
            "sort_order": 50,
            "is_active": True,
        },
    )
    if not status.is_active:
        status.is_active = True
        status.save(update_fields=["is_active"])

    return status, agenda_entry


def _gps_event_from_agenda_category(category):
    category = (category or "training").strip().lower()
    if category == "wedstrijd":
        return "competitiewedstrijd"
    if category in {"training", "kracht", "testing"}:
        return "opstart_training"
    return None


def _agenda_upload_suggestions(active_page, selected_team_code):
    today = timezone.localdate()
    start_date = today - timedelta(days=2)
    end_date = today + timedelta(days=7)
    data_team_codes = _academy_data_codes()
    selected_team_code = (selected_team_code or "").strip().upper()
    page_url_name = "wedstrijddata" if active_page == "wedstrijd" else "training"

    suggestions = []
    entries = (
        DayProgramEntry.objects
        .filter(date__gte=start_date, date__lte=end_date, team__in=data_team_codes)
        .exclude(category__iexact="rust")
        .order_by("date", "start_time", "id")
    )
    day_names = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
    for entry in entries:
        event_code = _gps_event_from_agenda_category(entry.category)
        if not event_code or event_code not in GPS_UPLOAD_EVENTS:
            continue
        event_label, session_kind = GPS_UPLOAD_EVENTS[event_code]
        target_page = "wedstrijd" if session_kind == "match" else "training"
        target_url = reverse("wedstrijddata" if target_page == "wedstrijd" else "training")
        team_code = (entry.team or "").strip().upper()
        date_label = f"{day_names[entry.date.weekday()]} {entry.date.strftime('%d-%m')}"
        suggestions.append(
            SimpleNamespace(
                team_code=team_code,
                team_label=_academy_team_label(team_code),
                event_code=event_code,
                event_label=event_label,
                date=entry.date,
                date_label=date_label,
                title=entry.title or event_label,
                target_page=target_page,
                href=f"{target_url}?team={team_code}&upload_event={event_code}",
                is_selected=team_code == selected_team_code and target_page == active_page,
            )
        )

    selected_event = None
    selected_suggestion = None
    for suggestion in suggestions:
        if suggestion.team_code == selected_team_code and suggestion.target_page == active_page:
            selected_event = suggestion.event_code
            selected_suggestion = suggestion
            break

    return {
        "suggestions": suggestions,
        "selected_event": selected_event,
        "selected_suggestion": selected_suggestion,
    }


def _agenda_week_items_by_day(team_code):
    team_code = (team_code or "").strip().upper()
    week_start = timezone.localdate() - timedelta(days=timezone.localdate().weekday())
    week_end = week_start + timedelta(days=6)
    items_by_day = {week_start + timedelta(days=offset): [] for offset in range(7)}
    if not team_code:
        return items_by_day

    entries = (
        DayProgramEntry.objects
        .filter(date__gte=week_start, date__lte=week_end, team__iexact=team_code)
        .order_by("date", "start_time", "id")
    )
    for entry in entries:
        items_by_day.setdefault(entry.date, []).append(
            SimpleNamespace(
                label=_agenda_category_label(entry.category),
                title=entry.title or _agenda_category_label(entry.category),
                start_time=entry.start_time,
                location=entry.location,
            )
        )
    return items_by_day


def _dashboard_week_url(date_value):
    if not date_value:
        return reverse("dashboard")
    week_start = date_value - timedelta(days=date_value.weekday())
    return f"{reverse('dashboard')}?week={week_start.isoformat()}"


def _upsert_injury_case(
    *,
    player,
    injury_type,
    start_date_value,
    duration_value,
    phase,
    expected_return_value=None,
    instance=None,
):
    started_on = parse_date(start_date_value) if isinstance(start_date_value, str) else start_date_value

    duration_days = None
    if duration_value not in (None, ""):
        try:
            duration_days = int(duration_value)
        except (TypeError, ValueError):
            duration_days = None

    expected_return_on = (
        parse_date(expected_return_value)
        if isinstance(expected_return_value, str) and expected_return_value.strip()
        else expected_return_value
    )
    if expected_return_on is None and started_on and duration_days is not None:
        expected_return_on = started_on + timedelta(days=duration_days)

    injury_type_obj = None
    if injury_type:
        injury_type_obj, _ = InjuryType.objects.get_or_create(name=injury_type.strip())

    phase_code = (phase or "").strip().lower()
    phase_defaults = {
        "early": "Vroege fase",
        "mid": "Middenfase",
        "final": "Laatste fase",
    }
    phase_obj = None
    if phase_code:
        phase_obj, _ = InjuryPhase.objects.get_or_create(
            code=phase_code,
            defaults={"label": phase_defaults.get(phase_code, phase_code.title())},
        )

    status_obj, _ = InjuryStatus.objects.get_or_create(
        code="active",
        defaults={"label": "Actief"},
    )

    injury = instance if instance is not None else InjuryCase(player=player)
    injury.player = player
    injury.injury_type_ref = injury_type_obj
    injury.phase_ref = phase_obj
    injury.started_on = started_on
    injury.expected_return_on = expected_return_on
    injury.status_ref = status_obj
    injury.save()
    return injury


# ---------- HOME / TEST ----------
def home(request):
    return HttpResponse("ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Django werkt correct!")


# ---------- DASHBOARD ----------
@login_required
def dashboard(request):
    player_app_user = _is_player_app_user(request.user)
    player_app_player = _player_for_user(request.user) if player_app_user else None
    player_app_preview_mode = request.GET.get("app_view") == "player" and not player_app_user
    player_app_tab = request.GET.get("player_tab")
    if player_app_tab not in {"wellness", "data", "testdata", "potential"}:
        player_app_tab = ""

    # ---------- BASIS ----------
    players_qs = Player.objects.select_related("monitoring_profile").all().order_by("name")
    if player_app_user:
        players_qs = players_qs.filter(id=player_app_player.id) if player_app_player else players_qs.none()
    players = list(players_qs)
    dayprograms = DayProgramEntry.objects.all().order_by("date")
    weekform = WeekProgramForm()

    # ---------- CLUBLOGOÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢S ----------
    logos = {
        "Willem II": "https://www.willem2.net/wp-content/uploads/willemii/Willem-II_logo_2022_2023.jpg",
        "Jong PSV": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/9983.png",
        "TOP Oss": "https://upload.wikimedia.org/wikipedia/en/d/de/TOP_Oss_FC.png",
        "FC Emmen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWu_AwBYFXF2byL4aPyBDxLRhzDETZXKgIeQ&s",
        "VVV-Venlo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/VVV_Venlo.svg/1096px-VVV_Venlo.svg.png",
        "FC Den Bosch": "https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/FC_Den_Bosch_logo.svg/1200px-FC_Den_Bosch_logo.svg.png",
        "FC Dordrecht": "https://upload.wikimedia.org/wikipedia/en/3/33/FC_Dordrecht.png",
        "SC Cambuur": "https://upload.wikimedia.org/wikipedia/commons/0/07/Wapen_SC_Cambuur.png",
        "Helmond Sport": "https://www.helmondsport.nl/wp-content/uploads/2024/02/logo-helmondsport-factuur.png",
        "ADO Den Haag": "https://upload.wikimedia.org/wikipedia/en/thumb/a/ad/ADO_Den_Haag_logo.svg/987px-ADO_Den_Haag_logo.svg.png",
        "FC Eindhoven": "https://www.fc-eindhovenav.nl/wp-content/uploads/fceindhovenav/FCEindhoven-logo-1.png",
        "Jong Ajax": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Logo_AFC_Ajax_%281928-1991%2C_2025-%29.png/330px-Logo_AFC_Ajax_%281928-1991%2C_2025-%29.png",
        "RKC Waalwijk": "https://upload.wikimedia.org/wikipedia/en/6/67/RKC_Waalwijk_logo.svg",
        "Jong FC Utrecht": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Logo_FC_Utrecht.svg",
        "Vitesse": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c8/SBV_Vitesse_logo.svg/960px-SBV_Vitesse_logo.svg.png",
        "MVV": "https://upload.wikimedia.org/wikipedia/it/9/92/MVV_Maastricht_logo.png",
        "De Graafschap": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOTZu6Zb8Ktkgj-RommON0Kw5tGAXD2mmwvw&s",
        "Jong AZ": "https://upload.wikimedia.org/wikipedia/en/6/6b/Jong_AZ_logo.png",
        "Roda": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e6/Roda_JC_logo.svg/1200px-Roda_JC_logo.svg.png",
        "Almere": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/Almere_City_FC_logo.svg/1200px-Almere_City_FC_logo.svg.png",
        "Roda JC": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e6/Roda_JC_logo.svg/1200px-Roda_JC_logo.svg.png",
        "Almere City FC": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/Almere_City_FC_logo.svg/1200px-Almere_City_FC_logo.svg.png",
    }

    # ---------- FORM HANDLING (WEEKPROGRAMMA + SEIZOENSIMPORT) ----------
    if request.method == "POST":
        if request.POST.get("form_type") in {"player_app_wellness", "player_app_srpe"}:
            date_obj = parse_date(request.POST.get("date", "")) or timezone.now().date()
            player_id = request.POST.get("player_id")
            player = get_object_or_404(Player, id=player_id)
            if player_app_user and (not player_app_player or player.id != player_app_player.id):
                raise PermissionDenied

            if request.POST.get("form_type") == "player_app_wellness":
                WellnessEntry.objects.update_or_create(
                    player=player,
                    date=date_obj,
                    defaults={
                        "sleep": _clean_int_or_none(request.POST.get("sleep")),
                        "mood": _clean_int_or_none(request.POST.get("mood")),
                        "fitness": _clean_int_or_none(request.POST.get("fitness")),
                        "soreness": _clean_int_or_none(request.POST.get("soreness")),
                        "comment": request.POST.get("comment", ""),
                    },
                )

            if request.POST.get("form_type") == "player_app_srpe":
                srpe = _clean_int_or_none(request.POST.get("srpe"))
                if srpe is not None:
                    RPEEntry.objects.update_or_create(
                        player=player,
                        date=date_obj,
                        defaults={"rpe": srpe},
                    )

            redirect_url = f"{reverse('dashboard')}?app_view=player&player_tab=wellness"
            if player_app_preview_mode:
                redirect_url = f"{redirect_url}&player_id={player.id}"
            return redirect(redirect_url)

        # ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ SEIZOENSPLANNING IMPORTEREN (harde reset)
        if request.POST.get("form_type") == "seed_matches":

            # Harde reset: verwijder alles (zo voorkom je oude foute wedstrijden zoals Eindhoven)
            Match.objects.all().delete()

            season_matches = [
                {"kickoff": datetime(2025, 11, 3, 20, 0), "home": "Jong PSV", "away": "Willem II"},
                {"kickoff": datetime(2025, 11, 7, 20, 0), "home": "Willem II", "away": "TOP Oss"},
                {"kickoff": datetime(2025, 11, 15, 21, 0), "home": "Willem II", "away": "FC Emmen"},
                {"kickoff": datetime(2025, 11, 21, 20, 0), "home": "VVV-Venlo", "away": "Willem II"},
                {"kickoff": datetime(2025, 11, 28, 20, 0), "home": "FC Den Bosch", "away": "Willem II"},
                {"kickoff": datetime(2025, 12, 6, 16, 30), "home": "Willem II", "away": "FC Dordrecht"},
                {"kickoff": datetime(2025, 12, 12, 20, 0), "home": "Willem II", "away": "SC Cambuur"},
                {"kickoff": datetime(2025, 12, 18, 21, 0), "home": "Willem II", "away": "Sparta Rotterdam"},
                {"kickoff": datetime(2025, 12, 21, 14, 30), "home": "Helmond Sport", "away": "Willem II"},
                {"kickoff": datetime(2026, 1, 9, 20, 0), "home": "Willem II", "away": "ADO Den Haag"},
                {"kickoff": datetime(2026, 1, 23, 20, 0), "home": "Willem II", "away": "VVV-Venlo"},
                {"kickoff": datetime(2026, 2, 2, 20, 0), "home": "Jong Ajax", "away": "Willem II"},
                {"kickoff": datetime(2026, 2, 8, 14, 30), "home": "Willem II", "away": "RKC Waalwijk"},
                {"kickoff": datetime(2026, 2, 16, 20, 0), "home": "Jong FC Utrecht", "away": "Willem II"},
                {"kickoff": datetime(2026, 2, 20, 20, 0), "home": "Willem II", "away": "Vitesse"},
                {"kickoff": datetime(2026, 2, 27, 20, 0), "home": "FC Emmen", "away": "Willem II"},
                {"kickoff": datetime(2026, 3, 8, 14, 30), "home": "Willem II", "away": "FC Den Bosch"},
                {"kickoff": datetime(2026, 3, 13, 20, 0), "home": "TOP Oss", "away": "Willem II"},
                {"kickoff": datetime(2026, 3, 22, 16, 45), "home": "MVV", "away": "Willem II"},
                {"kickoff": datetime(2026, 3, 27, 12, 0), "home": "Willem II", "away": "De Graafschap"},
                {"kickoff": datetime(2026, 4, 3, 20, 0), "home": "Willem II", "away": "Jong PSV"},
                {"kickoff": datetime(2026, 4, 6, 16, 45), "home": "Roda JC", "away": "Willem II"},
                {"kickoff": datetime(2026, 4, 12, 16, 45), "home": "Willem II", "away": "Almere City FC"},
                {"kickoff": datetime(2026, 4, 17, 20, 0), "home": "Willem II", "away": "Jong AZ"},
                {"kickoff": datetime(2026, 4, 24, 20, 0), "home": "FC Dordrecht", "away": "Willem II"},
            ]

            created_count = 0
            updated_count = 0  # blijft 0 door harde reset (functie behouden)

            for m in season_matches:
                kickoff = m["kickoff"]
                if timezone.is_naive(kickoff):
                    kickoff = timezone.make_aware(kickoff)

                home_team, _ = Team.objects.get_or_create(
                    name=m["home"],
                    defaults={"code": m["home"][:20].upper()},
                )
                away_team, _ = Team.objects.get_or_create(
                    name=m["away"],
                    defaults={"code": m["away"][:20].upper()},
                )

                Match.objects.create(
                    kickoff=kickoff,
                    home_team=home_team,
                    away_team=away_team,
                )
                created_count += 1

            messages.success(
                request,
                f"Seizoensplanning geÃƒÆ’Ã‚Â¯mporteerd. Nieuw: {created_count}, geÃƒÆ’Ã‚Â¼pdatet: {updated_count}, verwijderd: alles opnieuw opgebouwd.",
            )
            return redirect("dashboard")

        # ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Weekplanning opslaan
        if request.POST.get("form_type") == "add_weekday":
            weekform = WeekProgramForm(request.POST)
            if weekform.is_valid():
                weekform.save()
                messages.success(request, "Weekplanning succesvol toegevoegd.")
                return redirect("dashboard")

    # ---------- REVALIDATIES ----------
    rehab_players_qs = InjuryCase.objects.select_related(
        "player", "injury_type_ref", "phase_ref", "status_ref"
    ).order_by("-started_on")
    rehab_players = [_injury_to_ui(injury) for injury in rehab_players_qs]

    # ---------- GEMIDDELDE VETPERCENTAGE ----------
    avg_fat = None

    # ---------- KOMENDE WEDSTRIJD (UIT DATABASE) ----------
    now = timezone.now()
    upcoming_match = (
        Match.objects.select_related("home_team", "away_team")
        .filter(kickoff__gte=now)
        .order_by("kickoff")
        .first()
    )

    if upcoming_match:
        home_name = getattr(getattr(upcoming_match, "home_team", None), "name", "") or getattr(upcoming_match, "home", "")
        away_name = getattr(getattr(upcoming_match, "away_team", None), "name", "") or getattr(upcoming_match, "away", "")
    else:
        home_name = ""
        away_name = ""

    home_logo = logos.get(home_name, "") if upcoming_match else ""
    away_logo = logos.get(away_name, "") if upcoming_match else ""

    # ---------- MEETRAINERS JEUGD ----------
    youth_guests = YouthGuestWeek.objects.select_related("profile", "profile__team_ref").all().order_by("-week_of", "profile__name")

    # ---------- VERJAARDAGEN ----------
    birthdays = BirthdayRecord.objects.select_related("profile").all().order_by("date", "profile__name")

    # ---------- DASHBOARD ALERTS (WELLNESS + BELASTINGSRISICO) ----------
    today = timezone.now().date()
    week_start = today - timedelta(days=6)
    prev_start = today - timedelta(days=27)
    prev_end = today - timedelta(days=7)

    wellness_alerts = []
    today_wellness = WellnessEntry.objects.select_related("player").filter(date=today).order_by("player__name")
    for entry in today_wellness:
        reasons = []
        severity_points = 0
        if entry.sleep is not None and entry.sleep <= 2:
            reasons.append(f"slaap laag ({entry.sleep}/5)")
            severity_points += 2
        if entry.mood is not None and entry.mood <= 2:
            reasons.append(f"gevoel laag ({entry.mood}/5)")
            severity_points += 2
        if entry.fitness is not None and entry.fitness <= 2:
            reasons.append(f"fitheid laag ({entry.fitness}/5)")
            severity_points += 2
        if entry.soreness is not None and entry.soreness >= 4:
            reasons.append(f"spierpijn hoog ({entry.soreness}/5)")
            severity_points += 2
        if entry.comment and entry.comment.strip():
            reasons.append("opmerking ingevuld")
            severity_points += 1

        if reasons:
            if severity_points >= 6:
                level = "hoog"
            elif severity_points >= 3:
                level = "matig"
            else:
                level = "laag"
            wellness_alerts.append(
                {
                    "player_name": entry.player.name if entry.player else "-",
                    "reason": ", ".join(reasons),
                    "level": level,
                }
            )

    load_alerts = []
    recent_entries = (
        RPEEntry.objects.select_related("player")
        .filter(date__gte=prev_start, date__lte=today)
        .order_by("player__name", "date")
    )
    loads_by_player = {}
    for entry in recent_entries:
        if not entry.player_id:
            continue
        player_bucket = loads_by_player.setdefault(
            entry.player_id,
            {
                "name": entry.player.name if entry.player else "-",
                "current": [],
                "previous": [],
            },
        )
        # Prefer session load; fallback to simple rpe*100 proxy when load is empty.
        load_value = entry.session_load if entry.session_load is not None else (entry.rpe * 100 if entry.rpe is not None else None)
        if load_value is None:
            continue
        if entry.date >= week_start:
            player_bucket["current"].append(float(load_value))
        elif prev_start <= entry.date <= prev_end:
            player_bucket["previous"].append(float(load_value))

    for bucket in loads_by_player.values():
        current_vals = bucket["current"]
        prev_vals = bucket["previous"]
        if len(current_vals) < 2 or len(prev_vals) < 2:
            continue
        current_avg = sum(current_vals) / len(current_vals)
        prev_avg = sum(prev_vals) / len(prev_vals)
        if prev_avg <= 0:
            continue
        ratio = current_avg / prev_avg
        if ratio >= 1.35:
            if ratio >= 1.8:
                level = "hoog"
            elif ratio >= 1.5:
                level = "matig"
            else:
                level = "laag"
            load_alerts.append(
                {
                    "player_name": bucket["name"],
                    "current_avg": round(current_avg, 1),
                    "prev_avg": round(prev_avg, 1),
                    "ratio": round(ratio, 2),
                    "level": level,
                }
            )

    load_alerts = sorted(load_alerts, key=lambda item: item["ratio"], reverse=True)[:8]
    wellness_alerts = wellness_alerts[:8]

    total_risk_count = len(wellness_alerts) + len(load_alerts)
    highest_load_ratio = load_alerts[0]["ratio"] if load_alerts else None
    requested_week = parse_date(request.GET.get("week", ""))
    if requested_week is None:
        requested_week = today
    week_start_date = requested_week - timedelta(days=requested_week.weekday())
    week_end_date = week_start_date + timedelta(days=6)
    previous_week_start = week_start_date - timedelta(days=7)
    next_week_start = week_start_date + timedelta(days=7)
    current_week_dayprograms = (
        DayProgramEntry.objects.filter(date__gte=week_start_date, date__lte=week_end_date)
        .order_by("date")
    )
    day_labels = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
    week_agenda_days = []
    current_week_programs = list(current_week_dayprograms)
    for offset in range(7):
        day_date = week_start_date + timedelta(days=offset)
        week_agenda_days.append(
            {
                "date": day_date,
                "label": f"{day_labels[day_date.weekday()]} {day_date.strftime('%d-%m')}",
                "is_today": day_date == today,
                "items": [
                    SimpleNamespace(
                        entry=entry,
                        category_label=_agenda_category_label(entry.category),
                        css_category=(entry.category or "training").strip().lower(),
                    )
                    for entry in current_week_programs
                    if entry.date == day_date
                ],
            }
        )

    player_app_form_player = player_app_player
    if player_app_preview_mode:
        requested_player_id = request.GET.get("player_id")
        if requested_player_id:
            player_app_form_player = next((player for player in players if str(player.id) == str(requested_player_id)), None)
        if player_app_form_player is None and players:
            player_app_form_player = players[0]

    player_app_today = today
    player_app_is_potential = False
    player_app_potential_program = None
    player_app_potential_attention_notes = []
    player_app_potential_exercises = []
    player_app_potential_strength = {
        "thema": "",
        "frequentie": "",
        "doelstelling": "",
        "evaluatie": "",
    }
    player_app_today_wellness = None
    player_app_today_rpe = None
    player_app_gps_summary = {
        "sessions": 0,
        "load": 0,
        "distance_km": 0,
        "hsd_m": 0,
        "sprints": 0,
    }
    player_app_gps_recent = []
    player_app_latest_test = None
    player_app_recent_tests = []
    player_app_test_metrics = []
    player_app_test_trends = {"labels": [], "metrics": {}}
    if player_app_form_player:
        potential_section_key = f"player:{player_app_form_player.id}"
        player_app_is_potential = OverigNote.objects.filter(
            note_type="potential",
            page_key="potentials",
            section_key=potential_section_key,
        ).exists()
        if player_app_tab == "potential" and not player_app_is_potential:
            player_app_tab = ""
        if player_app_is_potential:
            player_app_potential_program = Programma.objects.filter(
                player=player_app_form_player
            ).order_by("-created_at").first()
            if player_app_potential_program:
                player_app_potential_exercises = list(
                    ProgrammaOefening.objects.select_related(
                        "naam_ref",
                        "frequentie_ref",
                        "duur_unit_ref",
                    ).filter(programma=player_app_potential_program).order_by("id")[:8]
                )

            attention_status_labels = {
                "open": "Open",
                "mee_bezig": "Mee bezig",
                "afgerond": "Afgerond",
            }
            for note in OverigNote.objects.filter(
                note_type="note",
                page_key="potentials",
                section_key=potential_section_key,
            ).order_by("-created_at", "-id")[:6]:
                parsed_note = {
                    "text": note.text,
                    "date": note.created_at.date(),
                    "owner": "",
                    "status_label": attention_status_labels["open"],
                }
                try:
                    saved_note = json.loads(note.text)
                except (TypeError, ValueError):
                    saved_note = None
                if isinstance(saved_note, dict):
                    status = saved_note.get("status")
                    parsed_note.update({
                        "text": saved_note.get("text") or "",
                        "date": parse_date(str(saved_note.get("date") or "")) or note.created_at.date(),
                        "owner": saved_note.get("owner") or "",
                        "status_label": attention_status_labels.get(status, attention_status_labels["open"]),
                    })
                player_app_potential_attention_notes.append(parsed_note)

            strength_note = OverigNote.objects.filter(
                note_type="section",
                page_key="potentials",
                section_key=f"strength:{player_app_form_player.id}",
            ).first()
            if strength_note and strength_note.text:
                try:
                    saved_strength = json.loads(strength_note.text)
                except (TypeError, ValueError):
                    saved_strength = None
                if isinstance(saved_strength, dict):
                    for key in player_app_potential_strength:
                        player_app_potential_strength[key] = saved_strength.get(key, "")

        player_app_today_wellness = WellnessEntry.objects.filter(
            player=player_app_form_player,
            date=player_app_today,
        ).first()
        player_app_today_rpe = RPEEntry.objects.filter(
            player=player_app_form_player,
            date=player_app_today,
        ).first()
        gps_since = today - timedelta(days=30)
        gps_rows = [
            row
            for row in fetch_performance_rows("training", player_app_form_player)
            if row.get("session_date") and row["session_date"] >= gps_since
        ]
        gps_rows.sort(key=lambda row: row["session_date"], reverse=True)
        total_load = sum(float(row.get("load") or 0) for row in gps_rows)
        total_distance = sum(float(row.get("total_distance") or 0) for row in gps_rows)
        total_hsd = sum(float(row.get("hsd") or 0) for row in gps_rows)
        total_sprints = sum(float(row.get("sprints") or 0) for row in gps_rows)
        player_app_gps_summary = {
            "sessions": len(gps_rows),
            "load": round(total_load, 0),
            "distance_km": round(total_distance / 1000, 1),
            "hsd_m": round(total_hsd, 0),
            "sprints": round(total_sprints, 0),
        }
        player_app_gps_recent = [
            {
                "date": row["session_date"],
                "load": round(float(row.get("load") or 0), 0),
                "distance_km": round(float(row.get("total_distance") or 0) / 1000, 1),
                "hsd_m": round(float(row.get("hsd") or 0), 0),
                "sprints": round(float(row.get("sprints") or 0), 0),
            }
            for row in gps_rows[:5]
        ]
        test_rows = [
            row
            for row in fetch_performance_rows("test", player_app_form_player)
            if row.get("session_date")
        ]
        test_rows.sort(key=lambda row: row["session_date"], reverse=True)
        if test_rows:
            latest_test = test_rows[0]
            player_app_latest_test = {
                "date": latest_test["session_date"],
                "sprint_10": latest_test.get("sprint_10"),
                "sprint_30": latest_test.get("sprint_30"),
                "cmj": latest_test.get("cmj"),
                "isrt": latest_test.get("isrt"),
                "submax": latest_test.get("submax"),
                "curr_weight": latest_test.get("curr_weight"),
                "length": latest_test.get("length"),
                "sum_skinfolds": latest_test.get("sum_skinfolds"),
            }
        test_rows_chronological = list(reversed(test_rows))

        def test_float(row, code):
            raw_value = row.get(code)
            if raw_value in (None, ""):
                return None
            try:
                return float(raw_value)
            except (TypeError, ValueError):
                return None

        test_metric_config = [
            {"code": "sprint_10", "label": "10 meter", "unit": "s", "lower_is_better": True},
            {"code": "sprint_30", "label": "30 meter", "unit": "s", "lower_is_better": True},
            {"code": "cmj", "label": "CMJ", "unit": "cm", "lower_is_better": False},
            {"code": "isrt", "label": "ISRT", "unit": "m", "lower_is_better": False},
            {"code": "curr_weight", "label": "Gewicht", "unit": "kg", "lower_is_better": False},
            {"code": "length", "label": "Lengte", "unit": "cm", "lower_is_better": False},
        ]
        player_app_test_trends = {
            "labels": [row["session_date"].strftime("%d-%m") for row in test_rows_chronological],
            "metrics": {},
        }
        for metric in test_metric_config:
            code = metric["code"]
            values = [test_float(row, code) for row in test_rows_chronological]
            real_values = [value for value in values if value is not None]
            latest_value = real_values[-1] if real_values else None
            previous_value = real_values[-2] if len(real_values) >= 2 else None
            change_value = None
            if latest_value is not None and previous_value is not None:
                change_value = previous_value - latest_value if metric["lower_is_better"] else latest_value - previous_value
            player_app_test_metrics.append({
                **metric,
                "latest": latest_value,
                "change": change_value,
                "has_data": latest_value is not None,
            })
            player_app_test_trends["metrics"][code] = {
                **metric,
                "values": values,
                "latest": latest_value,
                "change": change_value,
                "has_data": latest_value is not None,
            }

    # ---------- CONTEXT ----------
    context = {
        "title": "NEC Dashboard",
        "players": players,
        "dayprograms": dayprograms,
        "weekform": weekform,
        "rehab_players": rehab_players,
        "avg_fat": avg_fat,
        "upcoming_match": upcoming_match,
        "home_logo": home_logo,
        "away_logo": away_logo,
        "home_name": home_name,
        "away_name": away_name,
        "youth_guests": youth_guests,
        "birthdays": birthdays,
        "wellness_alerts": wellness_alerts,
        "load_alerts": load_alerts,
        "total_risk_count": total_risk_count,
        "highest_load_ratio": highest_load_ratio,
        "current_week_dayprograms": current_week_dayprograms,
        "week_agenda_days": week_agenda_days,
        "current_week_start": week_start_date,
        "current_week_end": week_end_date,
        "previous_week_url": f"{reverse('dashboard')}?week={previous_week_start.isoformat()}",
        "next_week_url": f"{reverse('dashboard')}?week={next_week_start.isoformat()}",
        "current_week_url": f"{reverse('dashboard')}?week={(today - timedelta(days=today.weekday())).isoformat()}",
        "player_app_player": player_app_player,
        "player_app_preview_mode": player_app_preview_mode,
        "player_app_tab": player_app_tab,
        "player_app_form_player": player_app_form_player,
        "player_app_is_potential": player_app_is_potential,
        "player_app_potential_program": player_app_potential_program,
        "player_app_potential_attention_notes": player_app_potential_attention_notes,
        "player_app_potential_exercises": player_app_potential_exercises,
        "player_app_potential_strength": player_app_potential_strength,
        "player_app_today": player_app_today,
        "player_app_today_wellness": player_app_today_wellness,
        "player_app_today_rpe": player_app_today_rpe,
        "player_app_gps_summary": player_app_gps_summary,
        "player_app_gps_recent": player_app_gps_recent,
        "player_app_latest_test": player_app_latest_test,
        "player_app_recent_tests": player_app_recent_tests,
        "player_app_test_metrics": player_app_test_metrics,
        "player_app_test_trends": player_app_test_trends,
    }

    return render(request, "Load_dashboard.html", context)




# ---------- WEEKPROGRAMMA BEWERKEN ----------
def edit_weekday(request, pk):
    day = get_object_or_404(DayProgramEntry, pk=pk)

    if request.method == "POST":
        form = WeekProgramForm(request.POST, instance=day)
        if form.is_valid():
            saved_day = form.save()
            messages.success(request, "Trainingsdag succesvol gewijzigd.")
            return redirect(_dashboard_week_url(saved_day.date))

    return redirect(_dashboard_week_url(day.date))


# ---------- WEEKPROGRAMMA VERWIJDEREN ----------
def delete_weekday(request, pk):
    day = get_object_or_404(DayProgramEntry, pk=pk)
    day_date = day.date
    if request.method == "POST":
        day.delete()
        messages.success(request, "Trainingsdag succesvol verwijderd.")
    return redirect(_dashboard_week_url(day_date))


# ---------- WEEKPROGRAMMA TOEVOEGEN ----------
def add_weekday(request):
    if request.method == "POST":
        form = WeekProgramForm(request.POST)
        if form.is_valid():
            saved_day = form.save()
            messages.success(request, "Trainingsdag succesvol toegevoegd.")
            return redirect(_dashboard_week_url(saved_day.date))

    return redirect("dashboard")


# ---------- BLESSURE TOEVOEGEN ----------
def add_rehab(request):
    if request.method == "POST":

        # Data ophalen uit de POST request
        name = request.POST.get("name")
        injury_type = request.POST.get("injury_type")
        start_date = request.POST.get("start_date")
        duration = request.POST.get("duration")
        phase = request.POST.get("phase")

        # Extra veiligheidscheck (modal verplicht al deze velden, maar dit is future-proof)
        if not name or not injury_type or not start_date or not duration or not phase:
            messages.error(request, "Alle velden zijn verplicht.")
            return redirect("dashboard")

        player_obj = _resolve_player_by_name(name)
        if player_obj is None:
            messages.error(request, "Speler niet gevonden. Voeg eerst de speler toe.")
            return redirect("dashboard")

        _upsert_injury_case(
            player=player_obj,
            injury_type=injury_type,
            start_date_value=start_date,
            duration_value=duration,
            phase=phase,
        )

        messages.success(request, f"Blessure van {player_obj.name} succesvol toegevoegd.")

    # Altijd terug naar dashboard
    return redirect("dashboard")


# ---------- VERJAARDAG TOEVOEGEN ----------
def add_birthday(request):
    if request.method == "POST":
        name = request.POST.get("name")
        role = request.POST.get("role") or None
        date = request.POST.get("date")

        if not name or not date:
            messages.error(request, "Naam en datum zijn verplicht.")
            return redirect("dashboard")

        profile, _ = BirthdayProfile.objects.get_or_create(name=name, role=role)
        BirthdayRecord.objects.get_or_create(
            profile=profile,
            date=date,
        )
        messages.success(request, f"Verjaardag van {name} toegevoegd.")

    return redirect("dashboard")


# ---------- VERJAARDAG VERWIJDEREN ----------
def delete_birthday(request, pk):
    if request.method == "POST":
        birthday = get_object_or_404(BirthdayRecord, pk=pk)
        birthday.delete()
        messages.success(request, "Verjaardag verwijderd.")

    return redirect("dashboard")


# ---------- MEETRAINER JEUGD TOEVOEGEN ----------
def add_youth_guest(request):
    if request.method == "POST":
        name = request.POST.get("name")
        team = request.POST.get("team") or None
        week_of = request.POST.get("week_of") or None

        if not name:
            messages.error(request, "Naam is verplicht.")
            return redirect("dashboard")

        profile = YouthGuestProfile(name=name)
        profile.team = team
        profile, _ = YouthGuestProfile.objects.get_or_create(
            name=name,
            team_ref=profile.team_ref,
        )
        YouthGuestWeek.objects.get_or_create(
            profile=profile,
            week_of=week_of,
        )
        messages.success(request, f"Meetrainer {name} toegevoegd.")

    return redirect("dashboard")


# ---------- MEETRAINER JEUGD VERWIJDEREN ----------
def delete_youth_guest(request, pk):
    if request.method == "POST":
        guest = get_object_or_404(YouthGuestWeek, pk=pk)
        guest.delete()
        messages.success(request, "Meetrainer verwijderd.")

    return redirect("dashboard")



# ---------- DATABASE SEED ----------
def seed_data(request):
    spelers = [
        "Nick Doodeman",
        "Raffael Behounek",
        "Justin Hoogma",
        "Mikael Tirpan",
        "Jari Schuurman",
        "Niels van Berkel",
    ]

    for naam in spelers:
        Player.objects.get_or_create(name=naam)

    return HttpResponse("Spelers toegevoegd.")


from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import (
    Player,
    NutritionDay,
    WeightEntry,
    NutritionIntakeSession,
    NutritionIntakeItem,
)



def nutrition_view(request):
    """
    Voedingsdashboard:
    - Weekvoedingsplanning (TEAM-wide)
    - Spelerselectie
    - Intake formulier (per speler)
    """

    # -----------------------------
    # Dagen + huidige dag
    # -----------------------------
    days = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
    current_day = days[datetime.now().weekday()]

    # -----------------------------
    # Spelers + geselecteerde speler
    # -----------------------------
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")

    player_id = request.GET.get("player_id")
    selected_player = None
    intake = None

    if player_id:
        selected_player = get_object_or_404(Player.objects.select_related("monitoring_profile"), id=player_id)
    else:
        selected_player = players.first()

    if selected_player:
        latest_session = (
            NutritionIntakeSession.objects
            .filter(player=selected_player)
            .prefetch_related("items")
            .order_by("-date", "-updated_at", "-id")
            .first()
        )
        if latest_session:
            item_map = {item.meal_key: item.value for item in latest_session.items.all()}
            intake = SimpleNamespace(
                date=latest_session.date,
                goal=latest_session.goal,
                breakfast=item_map.get("breakfast", ""),
                snack1=item_map.get("snack1", ""),
                lunch=item_map.get("lunch", ""),
                snack2=item_map.get("snack2", ""),
                dinner=item_map.get("dinner", ""),
                snack3=item_map.get("snack3", ""),
                supplements=item_map.get("supplements", ""),
                next_meeting_goal=latest_session.next_meeting_goal,
            )
        else:
            intake = None

    # -----------------------------
    # Zorg dat alle NutritionDay records bestaan
    # -----------------------------
    for d in days:
        NutritionDay.objects.get_or_create(day=d)

    # -----------------------------
    # POST afhandeling
    # -----------------------------
    if request.method == "POST":

        # =============================
        # 1) WEEKVOEDINGSSCHEMA SAVE
        # =============================
        if request.POST.get("nutrition_day") == "1":
            with transaction.atomic():
                for d in days:
                    meal = request.POST.get(f"meal_{d}", "").strip()
                    color = request.POST.get(f"color_{d}", "").strip() or None

                    NutritionDay.objects.update_or_create(
                        day=d,
                        defaults={"meal": meal, "color": color}
                    )

            messages.success(request, "Weekvoedingsschema is opgeslagen.")
            if player_id:
                return redirect(f"/nutrition/?player_id={player_id}")
            return redirect("/nutrition/")

        # =============================
        # 1b) SPELERGEWICHTEN OPSLAAN
        # =============================
        if request.POST.get("form_type") == "weights":
            updated = 0
            raw_date = request.POST.get("weight_date") or ""
            if raw_date:
                try:
                    weight_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:
                    weight_date = datetime.now().date()
            else:
                weight_date = datetime.now().date()
            with transaction.atomic():
                for player in players:
                    raw_weight = request.POST.get(f"weight_{player.id}", "").strip()
                    if raw_weight == "":
                        continue
                    try:
                        weight_val = float(raw_weight.replace(",", "."))
                    except ValueError:
                        continue

                    if weight_date == datetime.now().date():
                        profile = _get_or_create_monitoring_profile(player)
                        if profile.curr_weight is not None:
                            profile.prev_weight = profile.curr_weight
                        profile.curr_weight = weight_val
                        profile.save(update_fields=["prev_weight", "curr_weight", "updated_at"])

                    WeightEntry.objects.update_or_create(
                        player=player,
                        date=weight_date,
                        defaults={"weight": weight_val}
                    )
                    updated += 1

            if updated > 0:
                messages.success(request, f"Gewichten opgeslagen voor {updated} speler(s).")
            else:
                messages.warning(request, "Geen geldige gewichten om op te slaan.")

            if player_id:
                return redirect(f"/nutrition/?player_id={player_id}")
            return redirect("/nutrition/")

        # =============================
        # 2) PLAYER INTAKE SAVE
        # =============================
        post_player_id = request.POST.get("player_id")
        if post_player_id:
            p = get_object_or_404(Player, id=post_player_id)

            # Datum (input type="date") komt binnen als 'YYYY-MM-DD'
            raw_date = request.POST.get("date") or None
            parsed_date = None
            if raw_date:
                try:
                    parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:
                    parsed_date = None
                    messages.warning(request, "Datum kon niet worden gelezen. Gebruik het datumveld (YYYY-MM-DD).")
            else:
                parsed_date = datetime.now().date()

            with transaction.atomic():
                session, _ = NutritionIntakeSession.objects.update_or_create(
                    player=p,
                    date=parsed_date,
                    defaults={
                        "goal": request.POST.get("goal", "").strip(),
                        "next_meeting_goal": request.POST.get("next_meeting_goal", "").strip(),
                    },
                )
                meal_values = {
                    meal_key: request.POST.get(meal_key, "").strip()
                    for meal_key in ("breakfast", "snack1", "lunch", "snack2", "dinner", "snack3", "supplements")
                    if meal_key in request.POST
                }
                for meal_key, value in meal_values.items():
                    NutritionIntakeItem.objects.update_or_create(
                        session=session,
                        meal_key=meal_key,
                        defaults={"value": value},
                    )

                # Optioneel: nutrition_focus op Player model
                if "nutrition_focus" in request.POST:
                    profile = _get_or_create_monitoring_profile(p)
                    profile.nutrition_focus = request.POST.get("nutrition_focus", "").strip()
                    profile.save(update_fields=["nutrition_focus", "updated_at"])

            messages.success(request, f"Aandachtspunt voor {p.name} is opgeslagen.")
            return redirect(f"/nutrition/?player_id={p.id}")

        # Als POST wel komt maar geen herkenbare payload had:
        messages.warning(request, "Niets opgeslagen: ontbrekende POST-velden (player_id of nutrition_day).")
        if player_id:
            return redirect(f"/nutrition/?player_id={player_id}")
        return redirect("/nutrition/")

    for p_obj in players:
        profile = getattr(p_obj, "monitoring_profile", None)
        p_obj.monitor_prev_weight = profile.prev_weight if profile else None
        p_obj.monitor_curr_weight = profile.curr_weight if profile else None
        p_obj.monitor_sum_skinfolds = profile.sum_skinfolds if profile else None
        p_obj.monitor_nutrition_focus = profile.nutrition_focus if profile else ""
        if profile and profile.prev_weight is not None and profile.curr_weight is not None:
            p_obj.monitor_weight_diff = round(profile.curr_weight - profile.prev_weight, 1)
        else:
            p_obj.monitor_weight_diff = None

    if selected_player:
        selected_profile = getattr(selected_player, "monitoring_profile", None)
        selected_player.monitor_nutrition_focus = selected_profile.nutrition_focus if selected_profile else ""

    # -----------------------------
    # Data voor weekvoedingsschema
    # -----------------------------
    nutrition_days = {d: NutritionDay.objects.get(day=d) for d in days}

    # Refresh intake
    if selected_player:
        latest_session = (
            NutritionIntakeSession.objects
            .filter(player=selected_player)
            .prefetch_related("items")
            .order_by("-date", "-updated_at", "-id")
            .first()
        )
        if latest_session:
            item_map = {item.meal_key: item.value for item in latest_session.items.all()}
            intake = SimpleNamespace(
                date=latest_session.date,
                goal=latest_session.goal,
                breakfast=item_map.get("breakfast", ""),
                snack1=item_map.get("snack1", ""),
                lunch=item_map.get("lunch", ""),
                snack2=item_map.get("snack2", ""),
                dinner=item_map.get("dinner", ""),
                snack3=item_map.get("snack3", ""),
                supplements=item_map.get("supplements", ""),
                next_meeting_goal=latest_session.next_meeting_goal,
            )
        else:
            intake = None

    context = {
        "active_page": "nutrition",
        "days": days,
        "current_day": current_day,
        "players": players,
        "selected_player": selected_player,
        "nutrition_days": nutrition_days,
        "intake": intake,
    }
    return render(request, "nutrition.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify

from .models import AnthropometrySession, AnthropometryMeasurement



from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.text import slugify
from .models import Player, AnthropometrySession, AnthropometryMeasurement

def skinfold_view(request):
    """
    Antropometrische metingen:
    - Skinfolds
    - Girths
    - Algemene gegevens
    - Berekende vetpercentages (JS ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ hidden inputs)
    - Trend som skinfolds per speler (Chart.js)
    """

    # ======================
    # BASIS DATA
    # ======================
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")

    skinfold_sites = [
        "Triceps SF",
        "Subscapular SF",
        "Biceps SF",
        "Iliac crest SF",
        "Supraspinale SF",
        "Abdominale SF",
        "Thigh SF",
        "Calf SF",
    ]

    girth_sites = [
        "Arm relaxed girth",
        "Arm flexed & tensed girth",
        "Thigh middle girth",
        "Calf girth",
    ]

    formula_sites = [
        "Triceps SF",
        "Biceps SF",
        "Subscapular SF",
        "Iliac crest SF",
        "Supraspinale SF",
        "Abdominale SF",
    ]

    skinfold_field_map = {
        "Triceps SF": "triceps",
        "Biceps SF": "biceps",
        "Subscapular SF": "subscapular",
        "Iliac crest SF": "iliac_crest",
        "Supraspinale SF": "supraspinale",
        "Abdominale SF": "abdominal",
        "Thigh SF": "thigh",
        "Calf SF": "calf",
    }

    girth_field_map = {
        "Arm relaxed girth": "arm_relaxed",
        "Arm flexed & tensed girth": "arm_flexed",
        "Thigh middle girth": "thigh_girth",
        "Calf girth": "calf_girth",
    }

    def sync_anthropometry_v2(player_obj, measurement_date_raw, data_dict):
        measurement_date = parse_date(measurement_date_raw) if isinstance(measurement_date_raw, str) else measurement_date_raw
        if measurement_date is None:
            return

        def push_measurement(category, site_code, value, repetition):
            if value in (None, ""):
                return
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                return

            AnthropometryMeasurement.objects.create(
                session=session,
                category=category,
                site_code=site_code,
                repetition=repetition,
                value=numeric,
            )

        with transaction.atomic():
            session, _ = AnthropometrySession.objects.update_or_create(
                player=player_obj,
                date=measurement_date,
                defaults={
                    "body_mass": data_dict.get("body_mass"),
                    "length": data_dict.get("length"),
                    "fat_dw": data_dict.get("fat_dw"),
                    "fat_faulkner": data_dict.get("fat_faulkner"),
                    "fat_carter": data_dict.get("fat_carter"),
                    "fat_average": data_dict.get("fat_average"),
                },
            )

            AnthropometryMeasurement.objects.filter(session=session).delete()

            for _site_label, field in skinfold_field_map.items():
                push_measurement("skinfold", field, data_dict.get(f"{field}_m1"), 1)
                push_measurement("skinfold", field, data_dict.get(f"{field}_m2"), 2)
                push_measurement("skinfold", field, data_dict.get(f"{field}_m3"), 3)

            for _site_label, field in girth_field_map.items():
                push_measurement("girth", field, data_dict.get(f"{field}_m1"), 1)
                push_measurement("girth", field, data_dict.get(f"{field}_m2"), 2)
                push_measurement("girth", field, data_dict.get(f"{field}_m3"), 3)

    # ======================
    # POST ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ OPSLAAN
    # ======================
    if request.method == "POST":
        player_id = request.POST.get("player_id")
        measurement_date = request.POST.get("measurement_date")

        if not player_id or not measurement_date:
            messages.error(request, "Speler en datum zijn verplicht.")
            return redirect("huidplooimeting")

        player = get_object_or_404(Player, id=player_id)

        data = {
            "body_mass": request.POST.get("body_mass") or None,
            "length": request.POST.get("length") or None,
        }

        # ---- Skinfolds
        for site, field in skinfold_field_map.items():
            key = slugify(site)
            data[f"{field}_m1"] = request.POST.get(f"skinfold_{key}_m1") or None
            data[f"{field}_m2"] = request.POST.get(f"skinfold_{key}_m2") or None
            data[f"{field}_m3"] = request.POST.get(f"skinfold_{key}_m3") or None

        # ---- Girths
        for site, field in girth_field_map.items():
            key = slugify(site)
            data[f"{field}_m1"] = request.POST.get(f"girth_{key}_m1") or None
            data[f"{field}_m2"] = request.POST.get(f"girth_{key}_m2") or None
            data[f"{field}_m3"] = request.POST.get(f"girth_{key}_m3") or None

        # ---- Vetpercentages (hidden inputs vanuit JS)
        data["fat_dw"] = request.POST.get("fat_dw") or None
        data["fat_faulkner"] = request.POST.get("fat_faulkner") or None
        data["fat_carter"] = request.POST.get("fat_carter") or None
        data["fat_average"] = request.POST.get("fat_average") or None

        sync_anthropometry_v2(player, measurement_date, data)

        messages.success(request, f"Antropometrische metingen voor {player.name} zijn opgeslagen.")
        return redirect(f"{reverse('huidplooimeting')}?player={player.id}")

    # ======================
    # GET ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ DATA LADEN
    # ======================
    selected_player = None
    antropometry = None

    skinfold_rows = []
    girth_values = {}
    fat_values = {}

    # chart data voor de grafiek
    chart_labels = []
    chart_values = []

    # vergelijking: laatste vs vorige meting (8 sites)
    compare_labels = []
    compare_prev = []
    compare_last = []
    compare_prev_label = ""
    compare_last_label = ""

    # vergelijking laatste vs vorige meting (per site)
    compare_labels = []
    compare_prev = []
    compare_last = []
    compare_prev_label = ""
    compare_last_label = ""

    # helper: zelfde logica als je JS
    def sf_value(m1, m2, m3):
        if m3 is not None:
            return float(m3)
        if m1 is not None and m2 is not None:
            return (float(m1) + float(m2)) / 2
        if m1 is not None:
            return float(m1)
        if m2 is not None:
            return float(m2)
        return None

    def sum_skinfolds(a) -> float:
        total = 0.0
        for site in skinfold_sites:
            field = skinfold_field_map[site]
            v = sf_value(
                getattr(a, f"{field}_m1", None),
                getattr(a, f"{field}_m2", None),
                getattr(a, f"{field}_m3", None),
            )
            if v is not None:
                total += v
        return round(total, 1)

    def calculate_fat_values(a) -> dict:
        import math

        def site(site_name: str):
            field = skinfold_field_map[site_name]
            return sf_value(
                getattr(a, f"{field}_m1", None),
                getattr(a, f"{field}_m2", None),
                getattr(a, f"{field}_m3", None),
            )

        fat_dw = 0.0
        fat_faulkner = 0.0
        fat_carter = 0.0

        dw_sites = ["Triceps SF", "Biceps SF", "Subscapular SF", "Iliac crest SF"]
        dw_values = [site(s) for s in dw_sites]
        if all(v is not None and v > 0 for v in dw_values):
            sum_dw = sum(dw_values)
            density = 1.1631 - (0.0632 * math.log10(sum_dw))
            fat_dw = ((4.95 / density) - 4.5) * 100

        faulkner_sites = ["Triceps SF", "Subscapular SF", "Supraspinale SF", "Abdominale SF"]
        f_values = [site(s) for s in faulkner_sites]
        if all(v is not None and v > 0 for v in f_values):
            fat_faulkner = 5.783 + 0.153 * sum(f_values)

        sum_sf = sum_skinfolds(a)
        if sum_sf > 0:
            fat_carter = 2.585 + 0.1051 * sum_sf

        methods = [v for v in [fat_dw, fat_faulkner, fat_carter] if v > 0]
        fat_average = (sum(methods) / len(methods)) if methods else 0.0

        return {
            "dw": round(fat_dw, 1),
            "faulkner": round(fat_faulkner, 1),
            "carter": round(fat_carter, 1),
            "average": round(fat_average, 1),
        }

    def session_to_snapshot(session):
        values = {
            "date": session.date,
            "body_mass": session.body_mass,
            "length": session.length,
            "fat_dw": session.fat_dw,
            "fat_faulkner": session.fat_faulkner,
            "fat_carter": session.fat_carter,
            "fat_average": session.fat_average,
        }
        for m in session.measurements.all():
            values[f"{m.site_code}_m{m.repetition}"] = m.value
        return SimpleNamespace(**values)

    player_id = request.GET.get("player")

    if player_id:
        selected_player = Player.objects.filter(id=player_id).first()

        if selected_player:
            session_qs = (
                AnthropometrySession.objects
                .filter(player=selected_player)
                .prefetch_related("measurements")
                .order_by("date")
            )
            snapshots = [session_to_snapshot(s) for s in session_qs]

            if snapshots:
                antropometry = snapshots[-1]

            for snap in snapshots:
                chart_labels.append(snap.date.strftime("%Y-%m-%d"))
                chart_values.append(sum_skinfolds(snap))

            last_two = list(reversed(snapshots[-2:]))
            if len(last_two) >= 1:
                last_m = last_two[0]
                compare_last_label = last_m.date.strftime("%Y-%m-%d")
            if len(last_two) == 2:
                prev_m = last_two[1]
                compare_prev_label = prev_m.date.strftime("%Y-%m-%d")

            site_short = {
                "Triceps SF": "Triceps",
                "Subscapular SF": "Subscap",
                "Biceps SF": "Biceps",
                "Iliac crest SF": "Iliac",
                "Supraspinale SF": "Supra",
                "Abdominale SF": "Abdom",
                "Thigh SF": "Thigh",
                "Calf SF": "Calf",
            }

            if len(last_two) >= 1:
                for site in skinfold_sites:
                    field = skinfold_field_map[site]
                    compare_labels.append(site_short.get(site, site))
                    last_val = sf_value(
                        getattr(last_m, f"{field}_m1", None),
                        getattr(last_m, f"{field}_m2", None),
                        getattr(last_m, f"{field}_m3", None),
                    )
                    prev_val = None
                    if len(last_two) == 2:
                        prev_val = sf_value(
                            getattr(prev_m, f"{field}_m1", None),
                            getattr(prev_m, f"{field}_m2", None),
                            getattr(prev_m, f"{field}_m3", None),
                        )
                    compare_last.append(last_val if last_val is not None else None)
                    compare_prev.append(prev_val if prev_val is not None else None)

    # ---- Skinfold rows (ALTIJD opbouwen zodat je altijd kunt invullen)
    for site in skinfold_sites:
        field = skinfold_field_map[site]

        skinfold_rows.append({
            "site": site,
            "key": slugify(site),
            "m1": getattr(antropometry, f"{field}_m1", None) if antropometry else None,
            "m2": getattr(antropometry, f"{field}_m2", None) if antropometry else None,
            "m3": getattr(antropometry, f"{field}_m3", None) if antropometry else None,
        })

    # ---- Girths & vetpercentages (alleen als data bestaat)
    if antropometry:
        calculated_fat_values = calculate_fat_values(antropometry)

        for site, field in girth_field_map.items():
            key = slugify(site)
            girth_values[key] = {
                "m1": getattr(antropometry, f"{field}_m1", None),
                "m2": getattr(antropometry, f"{field}_m2", None),
                "m3": getattr(antropometry, f"{field}_m3", None),
            }

        fat_values = {
            "dw": antropometry.fat_dw if antropometry.fat_dw is not None else calculated_fat_values["dw"],
            "faulkner": antropometry.fat_faulkner if antropometry.fat_faulkner is not None else calculated_fat_values["faulkner"],
            "carter": antropometry.fat_carter if antropometry.fat_carter is not None else calculated_fat_values["carter"],
            "average": antropometry.fat_average if antropometry.fat_average is not None else calculated_fat_values["average"],
        }

    # ======================
    # CONTEXT
    # ======================
    context = {
        "active_page": "skinfolds",
        "players": players,

        "skinfold_sites": skinfold_sites,
        "girth_sites": girth_sites,
        "formula_sites": formula_sites,

        "selected_player": selected_player,
        "antropometry": antropometry,

        "skinfold_rows": skinfold_rows,
        "girth_values": girth_values,
        "fat_values": fat_values,

        # ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ¢â‚¬Ëœ voor de grafiek
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "compare_labels": compare_labels,
        "compare_prev": compare_prev,
        "compare_last": compare_last,
        "compare_prev_label": compare_prev_label,
        "compare_last_label": compare_last_label,
        "pdf_mode": request.GET.get("pdf") == "1",
    }

    return render(request, "huidplooimeting.html", context)


def huidplooimeting_pdf(request):
    if sync_playwright is None:
        return HttpResponse(
            "PDF-export is niet beschikbaar: installeer 'playwright' en voer 'playwright install' uit.",
            status=503,
        )

    player_id = request.GET.get("player")
    if not player_id:
        return HttpResponse("Geen speler geselecteerd", status=400)

    # ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Open dezelfde pagina maar in "pdf-mode"
    base_url = reverse("huidplooimeting")
    url = request.build_absolute_uri(f"{base_url}?player={player_id}&pdf=1")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Ga naar je bestaande pagina
        page.goto(url, wait_until="networkidle")

        # ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Wacht tot canvassen bestaan
        page.wait_for_selector("#skinfoldTrendChart", timeout=8000)
        page.wait_for_selector("#skinfoldCompareChart", timeout=8000)

        # ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Wacht tot Chart.js klaar is gerenderd + vetpercentage berekend
        page.wait_for_function("window.__skinfoldChartsDone === true", timeout=8000)
        page.wait_for_function("window.__fatReady === true", timeout=8000)

        # Extra zekerheid: event-loop even tijd geven
        page.wait_for_timeout(600)

        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={
                "top": "15mm",
                "bottom": "15mm",
                "left": "15mm",
                "right": "15mm",
            },
            prefer_css_page_size=True,
        )

        browser.close()

    response = HttpResponse(pdf_bytes, content_type="application/pdf")

    # ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ ATTACHMENT = echte download
    response["Content-Disposition"] = (
        f'attachment; filename="huidplooimeting_{player_id}.pdf"'
    )

    return response


from django.db.models import Avg

from django.db.models import Avg

from django.db.models import Avg, Sum

def training(request):
    import json
    import math
    from .models import TrainingWeekTarget

    player_app_user = _is_player_app_user(request.user)
    player_app_player = _player_for_user(request.user) if player_app_user else None

    metric_field_map = {
        "load": "load",
        "total_distance": "total_distance",
        "hsd": "hsd",
        "d20": "hsd",
        "sprints": "sprints",
        "max_speed": None,
        "d25": None,
        "acc": None,
        "dec": None,
    }
    selected_metric = request.GET.get("metric", "load")
    if selected_metric not in metric_field_map:
        selected_metric = "load"
    data_team_codes = _academy_data_codes()
    selected_data_team_code = (request.GET.get("team") or data_team_codes[0]).strip().upper()
    if selected_data_team_code not in data_team_codes:
        selected_data_team_code = data_team_codes[0]
    selected_data_team, team_players_qs = _team_players_for_gps_upload(selected_data_team_code)
    selected_data_team_label = selected_data_team.name if selected_data_team else _academy_team_label(selected_data_team_code)
    upload_agenda = _agenda_upload_suggestions("training", selected_data_team_code)
    selected_upload_event = request.GET.get("upload_event")
    if selected_upload_event not in GPS_UPLOAD_EVENTS:
        selected_upload_event = upload_agenda["selected_event"] or ""
    team_player_ids = set(team_players_qs.values_list("id", flat=True))
    selected_metric_field = metric_field_map[selected_metric]

    players_qs = Player.objects.select_related("monitoring_profile").all().order_by("name")
    if team_player_ids:
        players_qs = players_qs.filter(id__in=team_player_ids)
    else:
        players_qs = players_qs.none()
    if player_app_user:
        players_qs = players_qs.filter(id=player_app_player.id) if player_app_player else players_qs.none()
    players = list(players_qs)
    week_targets, _ = TrainingWeekTarget.objects.get_or_create(
        name=f"Geplande weektargets training {selected_data_team_code}"
    )
    agenda_week_items = _agenda_week_items_by_day(selected_data_team_code)

    day_field_map = [
        ("monday", "Maandag"),
        ("tuesday", "Dinsdag"),
        ("wednesday", "Woensdag"),
        ("thursday", "Donderdag"),
        ("friday", "Vrijdag"),
        ("saturday", "Zaterdag"),
        ("sunday", "Zondag"),
    ]
    metric_keys = [
        "total_distance",
        "d15",
        "d20",
        "d25",
        "acc",
        "dec",
    ]

    def parse_weektarget_value(raw_value):
        raw_value = (raw_value or "").strip()
        if not raw_value:
            return {key: "" for key in metric_keys}
        if "|" in raw_value:
            parts = raw_value.split("|")
            padded = (parts + [""] * len(metric_keys))[: len(metric_keys)]
            return {metric_keys[idx]: padded[idx] for idx in range(len(metric_keys))}
        return {
            "total_distance": raw_value,
            "d15": "",
            "d20": "",
            "d25": "",
            "acc": "",
            "dec": "",
        }

    def serialize_weektarget_value(prefix):
        return "|".join(
            (request.POST.get(f"{prefix}_{metric}", "") or "").strip()
            for metric in metric_keys
        )

    if request.method == "POST" and request.POST.get("save_weektargets") == "1":
        for field_name, _label in day_field_map:
            setattr(week_targets, field_name, serialize_weektarget_value(field_name))
        week_targets.save()
        messages.success(request, f"Geplande weektargets voor {selected_data_team_label} opgeslagen!")
        return redirect(f"{reverse('training')}?team={selected_data_team_code}")

    week_target_rows = [
        {
            "field_name": field_name,
            "label": label,
            "date": timezone.localdate() - timedelta(days=timezone.localdate().weekday()) + timedelta(days=index),
            "agenda_items": agenda_week_items.get(
                timezone.localdate() - timedelta(days=timezone.localdate().weekday()) + timedelta(days=index),
                [],
            ),
            "values": parse_weektarget_value(getattr(week_targets, field_name, "")),
        }
        for index, (field_name, label) in enumerate(day_field_map)
    ]
    rows = fetch_performance_rows("training", player_ids=team_player_ids)

    by_player = {}
    for row in rows:
        player_name = row["player_name"]
        agg = by_player.setdefault(
            player_name,
            {
                "player__name": player_name,
                "total_distance": 0.0,
                "total_hsd": 0.0,
                "total_sprints": 0.0,
                "total_load": 0.0,
                "loads": [],
            },
        )
        agg["total_distance"] += float(row.get("total_distance") or 0)
        agg["total_hsd"] += float(row.get("hsd") or 0)
        agg["total_sprints"] += float(row.get("sprints") or 0)
        cur_load = float(row.get("load") or 0)
        agg["total_load"] += cur_load
        agg["loads"].append(cur_load)

    player_summary = []
    for data in by_player.values():
        data["avg_load"] = mean(data["loads"])
        player_summary.append(data)
    player_summary.sort(key=lambda x: x["total_load"], reverse=True)

    chart_labels = [p["player__name"] for p in player_summary]
    chart_loads = [float(p["total_load"] or 0) for p in player_summary]
    chart_distances = [float(p["total_distance"] or 0) for p in player_summary]
    chart_hsd = [float(p["total_hsd"] or 0) for p in player_summary]
    chart_sprints = [float(p["total_sprints"] or 0) for p in player_summary]
    chart_d20 = chart_hsd[:]
    chart_d25 = [0.0 for _ in chart_labels]
    chart_acc = [0.0 for _ in chart_labels]
    chart_dec = [0.0 for _ in chart_labels]
    chart_max_speed = [0.0 for _ in chart_labels]

    avg_load = mean(chart_loads)
    avg_distance = mean(chart_distances)
    avg_sprints = mean(chart_sprints)

    all_training_data = [
        {
            "week": row.get("week"),
            "player__name": row["player_name"],
            "total_distance": float(row.get("total_distance") or 0),
            "hsd": float(row.get("hsd") or 0),
            "sprints": float(row.get("sprints") or 0),
            "load": float(row.get("load") or 0),
        }
        for row in sorted(rows, key=lambda r: (r.get("week") or 0, r["player_name"]))
    ]

    selected_player_name = request.GET.get("player")
    selected_player = players_qs.filter(name=selected_player_name).first() if selected_player_name else None
    trend_labels, trend_loads, trend_sprints = [], [], []
    if selected_player:
        week_group = {}
        for row in rows:
            if row["player_id"] != selected_player.id:
                continue
            week = row.get("week")
            if week is None:
                continue
            agg = week_group.setdefault(week, {"loads": [], "sprints": []})
            agg["loads"].append(float(row.get("load") or 0))
            agg["sprints"].append(float(row.get("sprints") or 0))
        for week in sorted(week_group.keys()):
            trend_labels.append(f"Wk {week}")
            trend_loads.append(mean(week_group[week]["loads"]))
            trend_sprints.append(mean(week_group[week]["sprints"]))

    def compute_ewma(values, lambda_val):
        result_list = []
        for i in range(len(values)):
            total = 0.0
            for j in range(i + 1):
                days_since = i - j
                weight = math.pow(1 - lambda_val, days_since)
                total += weight * float(values[j] or 0) * lambda_val
            result_list.append(total)
        return result_list

    lambda_acute = 2 / 8
    lambda_chronic = 2 / 29

    week_values = {}
    for row in rows:
        week = row.get("week")
        if week is None:
            continue
        values = week_values.setdefault(week, [])
        values.append(float(row.get(selected_metric_field) or 0) if selected_metric_field else 0.0)

    weeks = sorted(week_values.keys())
    metric_values = [mean(week_values[w]) for w in weeks]

    acute_values = compute_ewma(metric_values, lambda_acute)
    chronic_values = compute_ewma(metric_values, lambda_chronic)

    training_data = []
    for week in weeks:
        week_rows = [r for r in rows if r.get("week") == week]
        training_data.append(
            {
                "week": week,
                "total_distance": sum(float(r.get("total_distance") or 0) for r in week_rows),
                "hsd": sum(float(r.get("hsd") or 0) for r in week_rows),
                "sprints": sum(float(r.get("sprints") or 0) for r in week_rows),
                "load": sum(float(r.get("load") or 0) for r in week_rows),
            }
        )

    for i in range(len(training_data)):
        training_data[i]["d20"] = float(training_data[i]["hsd"] or 0)
        training_data[i]["d25"] = 0.0
        training_data[i]["acc"] = 0.0
        training_data[i]["dec"] = 0.0
        training_data[i]["max_speed"] = 0.0
        if i == 0:
            training_data[i]["acwr"] = None
        else:
            prev = training_data[i - 1]["load"] or 1
            training_data[i]["acwr"] = round(training_data[i]["load"] / prev, 2)

    daily_source = rows
    if selected_player:
        daily_source = [r for r in rows if r["player_id"] == selected_player.id]

    latest_session_date = max((r["session_date"] for r in daily_source), default=None)
    end_date = latest_session_date or timezone.localdate()
    start_date = end_date - timedelta(days=29)

    month_rows = {}
    points_by_date = {}
    for row in daily_source:
        session_date = row["session_date"]
        if session_date < start_date or session_date > end_date:
            continue

        agg = month_rows.setdefault(session_date, {"load": 0.0, "total_distance": 0.0, "hsd": 0.0, "sprints": 0.0})
        load_val = float(row.get("load") or 0)
        dist_val = float(row.get("total_distance") or 0)
        hsd_val = float(row.get("hsd") or 0)
        sprints_val = float(row.get("sprints") or 0)

        agg["load"] += load_val
        agg["total_distance"] += dist_val
        agg["hsd"] += hsd_val
        agg["sprints"] += sprints_val

        points = points_by_date.setdefault(
            session_date,
            {"points_load": [], "points_total_distance": [], "points_hsd": [], "points_sprints": []},
        )
        points["points_load"].append(load_val)
        points["points_total_distance"].append(dist_val)
        points["points_hsd"].append(hsd_val)
        points["points_sprints"].append(sprints_val)

    day_name_short = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
    day_buckets = []
    for offset in range(30):
        current_date = start_date + timedelta(days=offset)
        row = month_rows.get(current_date, {})
        points = points_by_date.get(current_date, {})
        day_buckets.append(
            {
                "day_label": f"{day_name_short[current_date.weekday()]} {current_date.strftime('%d-%m')}",
                "load": float(row.get("load") or 0),
                "total_distance": float(row.get("total_distance") or 0),
                "hsd": float(row.get("hsd") or 0),
                "sprints": float(row.get("sprints") or 0),
                "d20": float(row.get("hsd") or 0),
                "d25": 0.0,
                "acc": 0.0,
                "dec": 0.0,
                "max_speed": 0.0,
                "points_load": points.get("points_load", []),
                "points_total_distance": points.get("points_total_distance", []),
                "points_hsd": points.get("points_hsd", []),
                "points_d20": points.get("points_hsd", []),
                "points_sprints": points.get("points_sprints", []),
                "points_d25": [],
                "points_acc": [],
                "points_dec": [],
                "points_max_speed": [],
            }
        )

    context = {
        "players": players,
        "player_summary": player_summary,
        "chart_labels": json.dumps(chart_labels),
        "chart_loads": json.dumps(chart_loads),
        "chart_distances": json.dumps(chart_distances),
        "chart_hsd": json.dumps(chart_hsd),
        "chart_d20": json.dumps(chart_d20),
        "chart_d25": json.dumps(chart_d25),
        "chart_acc": json.dumps(chart_acc),
        "chart_dec": json.dumps(chart_dec),
        "chart_max_speed": json.dumps(chart_max_speed),
        "chart_sprints": json.dumps(chart_sprints),

        "avg_load": round(avg_load, 2),
        "avg_distance": round(avg_distance, 2),
        "avg_sprints": round(avg_sprints, 2),

        "trend_labels": json.dumps(trend_labels),
        "trend_loads": json.dumps(trend_loads),
        "trend_sprints": json.dumps(trend_sprints),
        "selected_player": selected_player,

        "weeks": json.dumps(weeks),
        "acute_values": json.dumps(acute_values),
        "chronic_values": json.dumps(chronic_values),
        "selected_metric": selected_metric,

        "all_training_data": all_training_data,
        "training_data": training_data,
        "training_data_json": training_data,
        "training_daily_data_json": day_buckets,
        "training_daily_range_label": f"{start_date.strftime('%d-%m-%Y')} t/m {end_date.strftime('%d-%m-%Y')}",
        "week_targets": week_targets,
        "week_target_rows": week_target_rows,
        "upload_team_codes": data_team_codes,
        "upload_events": GPS_UPLOAD_EVENTS,
        "selected_upload_event": selected_upload_event,
        "agenda_upload_suggestions": upload_agenda["suggestions"],
        "selected_agenda_upload_suggestion": upload_agenda["selected_suggestion"],
        "data_team_codes": data_team_codes,
        "data_team_options": _academy_data_team_options(),
        "selected_data_team_code": selected_data_team_code,
        "selected_data_team_label": selected_data_team_label,
        "data_team_query": f"team={selected_data_team_code}",
        "show_import_log": _is_admin_user(request.user),
        "latest_import_logs": _latest_admin_import_logs(request),

        "active_page": "training",
    }

    return render(request, "Training.html", context)


def wedstrijddata(request):
    import json

    metric_field_map = {
        "load": "load",
        "total_distance": "total_distance",
        "hsd": "hsd",
        "d20": "hsd",
        "sprints": "sprints",
        "d25": "his",
        "acc": "accelerations",
        "dec": "decelerations",
        "max_speed": None,
    }
    selected_metric = request.GET.get("metric", "load")
    if selected_metric not in metric_field_map:
        selected_metric = "load"
    data_team_codes = _academy_data_codes()
    selected_data_team_code = (request.GET.get("team") or data_team_codes[0]).strip().upper()
    if selected_data_team_code not in data_team_codes:
        selected_data_team_code = data_team_codes[0]
    selected_data_team, team_players_qs = _team_players_for_gps_upload(selected_data_team_code)
    selected_data_team_label = selected_data_team.name if selected_data_team else _academy_team_label(selected_data_team_code)
    upload_agenda = _agenda_upload_suggestions("wedstrijd", selected_data_team_code)
    selected_upload_event = request.GET.get("upload_event")
    if selected_upload_event not in GPS_UPLOAD_EVENTS:
        selected_upload_event = upload_agenda["selected_event"] or ""
    team_player_ids = set(team_players_qs.values_list("id", flat=True))

    POSITION_TARGETS = {
        "Spits": {"km": 11.5, "hir": 950, "his": 200, "a_d": 180},
        "Targetman": {"km": 11, "hir": 500, "his": 75, "a_d": 160},
        "Buitenspeler": {"km": 11, "hir": 1000, "his": 150, "a_d": 150},
        "Dynamische middenvelder": {"km": 12, "hir": 950, "his": 200, "a_d": 180},
        "Controlerende middenvelder": {"km": 12, "hir": 700, "his": 150, "a_d": 180},
        "Centrale verdediger": {"km": 10.5, "hir": 500, "his": 100, "a_d": 160},
        "Vleugelverdediger": {"km": 11, "hir": 1000, "his": 250, "a_d": 190},
    }

    players = Player.objects.select_related("monitoring_profile").filter(id__in=team_player_ids).order_by("name")
    selected_player_name = request.GET.get("player")
    selected_player = players.filter(name=selected_player_name).first() if selected_player_name else None

    all_rows = fetch_performance_rows("match", player_ids=team_player_ids)
    match_rows = [r for r in all_rows if (not selected_player or r["player_id"] == selected_player.id)]
    match_rows.sort(key=lambda r: ((r.get("week") or 0), r["session_date"]), reverse=True)

    last_5_rows = list(reversed(match_rows[:5]))
    last_5_matches = [
        SimpleNamespace(
            week=row.get("week"),
            total_distance=float(row.get("total_distance") or 0),
            hsd=float(row.get("hsd") or 0),
            sprints=float(row.get("sprints") or 0),
            load=float(row.get("load") or 0),
            his=float(row.get("his") or 0),
            accelerations=float(row.get("accelerations") or 0),
            decelerations=float(row.get("decelerations") or 0),
        )
        for row in last_5_rows
    ]

    if last_5_matches:
        avg_stats = {
            "avg_distance": mean(m.total_distance for m in last_5_matches),
            "avg_hsd": mean(m.hsd for m in last_5_matches),
            "avg_sprints": mean(m.sprints for m in last_5_matches),
            "avg_load": mean(m.load for m in last_5_matches),
        }
        top_stats = {
            "top_distance": max(m.total_distance for m in last_5_matches),
            "top_hsd": max(m.hsd for m in last_5_matches),
            "top_sprints": max(m.sprints for m in last_5_matches),
            "top_load": max(m.load for m in last_5_matches),
        }
    else:
        avg_stats, top_stats = {}, {}

    selected_position_name = (
        selected_player.position_ref.name
        if selected_player and selected_player.position_ref
        else None
    )
    position_targets = POSITION_TARGETS.get(selected_position_name) if selected_position_name else None

    match_labels = [f"WK {m.week}" if m.week else "-" for m in last_5_matches]
    match_km = [float(m.total_distance or 0) for m in last_5_matches]
    match_hir = [float(m.hsd or 0) for m in last_5_matches]
    match_sprints = [float(m.sprints or 0) for m in last_5_matches]
    match_load = [float(m.load or 0) for m in last_5_matches]
    match_d20 = [float(m.hsd or 0) for m in last_5_matches]
    match_d25 = [float(m.his or 0) for m in last_5_matches]
    match_acc = [float(m.accelerations or 0) for m in last_5_matches]
    match_dec = [float(m.decelerations or 0) for m in last_5_matches]
    match_max_speed = [0.0 for _ in last_5_matches]

    weeks = [r.get("week") for r in all_rows if r.get("week") is not None]
    last_week = max(weeks) if weeks else None
    team_rows = [r for r in all_rows if last_week is not None and r.get("week") == last_week]

    grouped = {}
    for row in team_rows:
        name = row["player_name"]
        agg = grouped.setdefault(
            name,
            {"player__name": name, "km": 0.0, "hir": 0.0, "sprints": 0.0, "his": 0.0, "load": 0.0, "acc": 0.0, "dec": 0.0},
        )
        agg["km"] += float(row.get("total_distance") or 0)
        agg["hir"] += float(row.get("hsd") or 0)
        agg["sprints"] += float(row.get("sprints") or 0)
        agg["his"] += float(row.get("his") or 0)
        agg["load"] += float(row.get("load") or 0)
        agg["acc"] += float(row.get("accelerations") or 0)
        agg["dec"] += float(row.get("decelerations") or 0)

    last_team_rows = [grouped[k] for k in sorted(grouped.keys())]

    team_labels = [row["player__name"] for row in last_team_rows]
    team_distance = [float(row["km"] or 0) for row in last_team_rows]
    team_hsd = [float(row["hir"] or 0) for row in last_team_rows]
    team_sprints = [float(row["sprints"] or 0) for row in last_team_rows]
    team_his = [float(row["his"] or 0) for row in last_team_rows]
    team_load = [float(row["load"] or 0) for row in last_team_rows]
    team_acc = [float(row["acc"] or 0) for row in last_team_rows]
    team_dec = [float(row["dec"] or 0) for row in last_team_rows]
    team_d20 = team_hsd[:]
    team_d25 = team_his[:]
    team_max_speed = [0.0 for _ in last_team_rows]

    context = {
        "players": players,
        "selected_player": selected_player,
        "selected_metric": selected_metric,
        "last_5_matches": last_5_matches,
        "avg_stats": avg_stats,
        "top_stats": top_stats,
        "targets": position_targets,

        "match_labels": match_labels,
        "match_km": match_km,
        "match_hir": match_hir,
        "match_his": match_d25,
        "match_sprints": match_sprints,
        "match_load": match_load,
        "match_d20": match_d20,
        "match_d25": match_d25,
        "match_acc": match_acc,
        "match_dec": match_dec,
        "match_max_speed": match_max_speed,

        "team_labels": team_labels,
        "team_distance": team_distance,
        "team_hsd": team_hsd,
        "team_sprints": team_sprints,
        "team_his": team_his,
        "team_load": team_load,
        "team_acc": team_acc,
        "team_dec": team_dec,
        "team_d20": team_d20,
        "team_d25": team_d25,
        "team_max_speed": team_max_speed,
        "upload_team_codes": data_team_codes,
        "upload_events": GPS_UPLOAD_EVENTS,
        "selected_upload_event": selected_upload_event,
        "agenda_upload_suggestions": upload_agenda["suggestions"],
        "selected_agenda_upload_suggestion": upload_agenda["selected_suggestion"],
        "data_team_codes": data_team_codes,
        "data_team_options": _academy_data_team_options(),
        "selected_data_team_code": selected_data_team_code,
        "selected_data_team_label": selected_data_team_label,
        "data_team_query": f"team={selected_data_team_code}",
        "show_import_log": _is_admin_user(request.user),
        "latest_import_logs": _latest_admin_import_logs(request),

        "active_page": "wedstrijd",
    }

    return render(request, "Training.html", context)


def fysiek_rapport(request):
    import json

    players = Player.objects.select_related("monitoring_profile", "position_ref").all().order_by("name")
    report_team_codes = _academy_data_codes()
    selected_team_code = (request.GET.get("team") or report_team_codes[0]).strip().upper()
    if selected_team_code not in report_team_codes:
        selected_team_code = report_team_codes[0]
    selected_team, team_players = _team_players_for_gps_upload(selected_team_code)
    selected_team_label = selected_team.name if selected_team else _academy_team_label(selected_team_code)
    team_player_ids = set(team_players.values_list("id", flat=True))
    training_rows_all = fetch_performance_rows("training", player_ids=team_player_ids)
    match_rows_all = fetch_performance_rows("match", player_ids=team_player_ids)
    all_dates = [row["session_date"] for row in training_rows_all + match_rows_all if row.get("session_date")]
    report_end = max(all_dates) if all_dates else timezone.localdate()
    report_start = report_end - timedelta(days=6)

    def in_report_week(row):
        session_date = row.get("session_date")
        return session_date and report_start <= session_date <= report_end

    training_rows = [row for row in training_rows_all if in_report_week(row)]
    match_rows = [row for row in match_rows_all if in_report_week(row)]
    combined_rows = [*training_rows, *match_rows]

    def val(row, key):
        return float(row.get(key) or 0)

    def sum_metric(rows, key):
        return sum(val(row, key) for row in rows)

    total_load = sum_metric(combined_rows, "load")
    total_distance = sum_metric(combined_rows, "total_distance")
    total_hsd = sum_metric(combined_rows, "hsd")
    total_sprints = sum_metric(combined_rows, "sprints")
    match_his = sum_metric(match_rows, "his")
    match_acc = sum_metric(match_rows, "accelerations")
    match_dec = sum_metric(match_rows, "decelerations")

    active_player_ids = {row["player_id"] for row in combined_rows}
    avg_load_per_player = total_load / len(active_player_ids) if active_player_ids else 0

    player_map = {}
    for row in combined_rows:
        data = player_map.setdefault(
            row["player_name"],
            {
                "name": row["player_name"],
                "total_distance": 0.0,
                "hsd": 0.0,
                "his": 0.0,
                "sprints": 0.0,
                "load": 0.0,
                "accelerations": 0.0,
                "decelerations": 0.0,
                "first_half_load": 0.0,
                "second_half_load": 0.0,
            },
        )
        data["total_distance"] += val(row, "total_distance")
        data["hsd"] += val(row, "hsd")
        data["his"] += val(row, "his")
        data["sprints"] += val(row, "sprints")
        data["load"] += val(row, "load")
        data["accelerations"] += val(row, "accelerations")
        data["decelerations"] += val(row, "decelerations")
        if row in match_rows:
            first_half = val(row, "first_half_load")
            second_half = val(row, "second_half_load")
            if first_half or second_half:
                data["first_half_load"] += first_half
                data["second_half_load"] += second_half
            else:
                fallback_half_load = val(row, "load") / 2
                data["first_half_load"] += fallback_half_load
                data["second_half_load"] += fallback_half_load

    player_report_rows = sorted(player_map.values(), key=lambda item: item["load"], reverse=True)
    top_player_rows = player_report_rows[:12]

    day_names = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
    daily_labels = []
    daily_training_load = []
    daily_match_load = []
    daily_total_distance = []
    daily_hsd = []
    daily_his = []
    daily_sprints = []
    daily_acc_dec = []
    session_buckets = []
    for offset in range(7):
        current_date = report_start + timedelta(days=offset)
        daily_labels.append(f"{day_names[current_date.weekday()]} {current_date.strftime('%d-%m')}")
        day_training_rows = [row for row in training_rows if row["session_date"] == current_date]
        day_match_rows = [row for row in match_rows if row["session_date"] == current_date]
        day_combined_rows = [*day_training_rows, *day_match_rows]
        daily_training_load.append(round(sum_metric(day_training_rows, "load"), 1))
        daily_match_load.append(round(sum_metric(day_match_rows, "load"), 1))
        daily_total_distance.append(round(sum_metric(day_combined_rows, "total_distance") / 1000, 2))
        daily_hsd.append(round(sum_metric(day_combined_rows, "hsd") / 1000, 2))
        daily_his.append(round(sum_metric(day_match_rows, "his") / 1000, 2))
        daily_sprints.append(round(sum_metric(day_combined_rows, "sprints"), 0))
        daily_acc_dec.append(round(sum_metric(day_match_rows, "accelerations") + sum_metric(day_match_rows, "decelerations"), 0))
        for label, rows_for_session in (("Training", day_training_rows), ("Wedstrijd", day_match_rows)):
            if not rows_for_session:
                continue
            session_buckets.append(
                {
                    "label": f"{day_names[current_date.weekday()]} {current_date.strftime('%d-%m')} {label}",
                    "load": round(sum_metric(rows_for_session, "load"), 1),
                    "distance": round(sum_metric(rows_for_session, "total_distance") / 1000, 2),
                    "hsd": round(sum_metric(rows_for_session, "hsd") / 1000, 2),
                    "his": round(sum_metric(rows_for_session, "his") / 1000, 2),
                    "sprints": round(sum_metric(rows_for_session, "sprints"), 0),
                    "accdec": round(sum_metric(rows_for_session, "accelerations") + sum_metric(rows_for_session, "decelerations"), 0),
                }
            )

    report_summary = {
        "range_label": f"{report_start.strftime('%d-%m-%Y')} t/m {report_end.strftime('%d-%m-%Y')}",
        "training_sessions": len(training_rows),
        "match_sessions": len(match_rows),
        "active_players": len(active_player_ids),
        "total_load": round(total_load, 0),
        "total_distance_km": round(total_distance / 1000, 1),
        "total_hsd_km": round(total_hsd / 1000, 1),
        "match_his_km": round(match_his / 1000, 1),
        "total_sprints": round(total_sprints, 0),
        "avg_load_per_player": round(avg_load_per_player, 0),
        "match_acc_dec": round(match_acc + match_dec, 0),
    }

    context = {
        "players": players,
        "active_page": "rapport",
        "report_team_codes": report_team_codes,
        "report_team_options": _academy_data_team_options(),
        "selected_team_code": selected_team_code,
        "selected_team_label": selected_team_label,
        "selected_data_team_code": selected_team_code,
        "report_summary": report_summary,
        "player_report_rows": player_report_rows[:10],
        "report_daily_labels": json.dumps(daily_labels),
        "report_daily_training_load": json.dumps(daily_training_load),
        "report_daily_match_load": json.dumps(daily_match_load),
        "report_daily_total_distance": json.dumps(daily_total_distance),
        "report_daily_hsd": json.dumps(daily_hsd),
        "report_daily_his": json.dumps(daily_his),
        "report_daily_sprints": json.dumps(daily_sprints),
        "report_daily_acc_dec": json.dumps(daily_acc_dec),
        "report_session_labels": json.dumps([row["label"] for row in session_buckets]),
        "report_session_load": json.dumps([row["load"] for row in session_buckets]),
        "report_session_distance": json.dumps([row["distance"] for row in session_buckets]),
        "report_session_hsd": json.dumps([row["hsd"] for row in session_buckets]),
        "report_session_his": json.dumps([row["his"] for row in session_buckets]),
        "report_session_sprints": json.dumps([row["sprints"] for row in session_buckets]),
        "report_session_acc_dec": json.dumps([row["accdec"] for row in session_buckets]),
        "report_player_labels": json.dumps([row["name"] for row in top_player_rows]),
        "report_player_load": json.dumps([round(row["load"], 1) for row in top_player_rows]),
        "report_player_distance": json.dumps([round(row["total_distance"] / 1000, 2) for row in top_player_rows]),
        "report_half_player_labels": json.dumps([row["name"] for row in top_player_rows]),
        "report_first_half_load": json.dumps([round(row["first_half_load"], 1) for row in top_player_rows]),
        "report_second_half_load": json.dumps([round(row["second_half_load"], 1) for row in top_player_rows]),
    }

    return render(request, "Training.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Min, Max


def testdata(request):

    def calculate_percentile(value, min_val, max_val, reverse=False):
        if value is None or min_val is None or max_val is None:
            return None
        if min_val == max_val:
            return 50
        if reverse:
            return round(100 * (max_val - value) / (max_val - min_val))
        return round(100 * (value - min_val) / (max_val - min_val))

    data_team_codes = _academy_data_codes()
    player_id = request.GET.get("player_id")
    player_only_mode = _is_player_app_user(request.user)
    if player_only_mode:
        player_for_user = _player_for_user(request.user)
        if not player_for_user:
            raise PermissionDenied
        if player_id and str(player_id) != str(player_for_user.id):
            raise PermissionDenied
        player_id = str(player_for_user.id)

    def team_code_for_player(player_id_value):
        if not player_id_value:
            return ""
        today = timezone.localdate()
        assignment = (
            PlayerTeamAssignment.objects
            .select_related("team")
            .filter(
                player_id=player_id_value,
                team__code__in=data_team_codes,
                start_date__lte=today,
            )
            .filter(Q(end_date__isnull=True) | Q(end_date__gte=today))
            .order_by("-start_date", "-id")
            .first()
        )
        return assignment.team.code if assignment and assignment.team else ""

    selected_team_code = (
        request.GET.get("team")
        or request.POST.get("team")
        or team_code_for_player(player_id)
        or data_team_codes[0]
    ).strip().upper()
    if selected_team_code not in data_team_codes:
        selected_team_code = data_team_codes[0]
    selected_team, team_players_qs = _team_players_for_gps_upload(selected_team_code)
    selected_team_label = selected_team.name if selected_team else _academy_team_label(selected_team_code)
    players = list(team_players_qs.select_related("monitoring_profile", "position_ref"))
    team_player_ids = {player.id for player in players}
    team_test_rows = fetch_performance_rows("test", player_ids=team_player_ids)
    test_rows = team_test_rows

    test_data = [
        SimpleNamespace(
            player=row["player_obj"],
            test_date=row["session_date"],
            sprint_10=row.get("sprint_10"),
            sprint_30=row.get("sprint_30"),
            cmj=row.get("cmj"),
            isrt=row.get("isrt"),
            submax=row.get("submax"),
            curr_weight=row.get("curr_weight"),
            length=row.get("length"),
            sum_skinfolds=row.get("sum_skinfolds"),
        )
        for row in team_test_rows
    ]

    # Teamoverzicht voor tab "Testdata bekijken" zonder geselecteerde speler
    speed_by_player = {}
    for speed_row in PlayerSpeedTest.objects.values("player_id", "mss_kmh"):
        player_key = speed_row["player_id"]
        mss = speed_row.get("mss_kmh")
        if player_key is None or mss is None:
            continue
        mss_float = float(mss)
        prev = speed_by_player.get(player_key)
        if prev is None or mss_float > prev:
            speed_by_player[player_key] = mss_float

    metrics_by_player = {}
    for row in team_test_rows:
        pid = row["player_id"]
        bucket = metrics_by_player.setdefault(pid, {"isrt": None, "max_hr": None})
        isrt_val = row.get("isrt")
        max_hr_val = row.get("max_hr")
        if isrt_val is not None:
            isrt_f = float(isrt_val)
            if bucket["isrt"] is None or isrt_f > bucket["isrt"]:
                bucket["isrt"] = isrt_f
        if max_hr_val is not None:
            hr_f = float(max_hr_val)
            if bucket["max_hr"] is None or hr_f > bucket["max_hr"]:
                bucket["max_hr"] = hr_f

    team_profile_rows = []
    for p in players:
        metric_bucket = metrics_by_player.get(p.id, {})
        team_profile_rows.append(
            {
                "name": p.name,
                "max_speed": speed_by_player.get(p.id),
                "isrt": metric_bucket.get("isrt"),
                "max_hr": metric_bucket.get("max_hr"),
            }
        )

    def metric_values(code):
        vals = []
        for row in team_test_rows:
            raw = row.get(code)
            if raw is not None:
                vals.append(float(raw))
        return vals

    sprint10_vals = metric_values("sprint_10")
    sprint30_vals = metric_values("sprint_30")
    cmj_vals = metric_values("cmj")
    isrt_vals = metric_values("isrt")
    submax_vals = metric_values("submax")

    team_min = {
        "sprint10_min": min(sprint10_vals) if sprint10_vals else None,
        "sprint30_min": min(sprint30_vals) if sprint30_vals else None,
        "cmj_min": min(cmj_vals) if cmj_vals else None,
        "isrt_min": min(isrt_vals) if isrt_vals else None,
        "submax_min": min(submax_vals) if submax_vals else None,
    }
    team_max = {
        "sprint10_max": max(sprint10_vals) if sprint10_vals else None,
        "sprint30_max": max(sprint30_vals) if sprint30_vals else None,
        "cmj_max": max(cmj_vals) if cmj_vals else None,
        "isrt_max": max(isrt_vals) if isrt_vals else None,
        "submax_max": max(submax_vals) if submax_vals else None,
    }

    tab_param = (request.GET.get("tab") or "").strip().lower()
    if tab_param not in {"invoer", "profiel"}:
        tab_param = "profiel" if player_id else "invoer"
    if player_only_mode:
        tab_param = "profiel"
    selected_player = None
    percentiles = {}

    if player_id:
        selected_player = get_object_or_404(Player.objects.select_related("monitoring_profile", "position_ref"), id=player_id)
        player_rows = [r for r in test_rows if r["player_id"] == selected_player.id]
        player_rows.sort(key=lambda r: r["session_date"], reverse=True)
        latest = player_rows[0] if player_rows else None
        selected_player.latest_test = SimpleNamespace(**latest) if latest else None

        if latest:
            percentiles = {
                "sprint_10": calculate_percentile(latest.get("sprint_10"), team_min["sprint10_min"], team_max["sprint10_max"], reverse=True),
                "sprint_30": calculate_percentile(latest.get("sprint_30"), team_min["sprint30_min"], team_max["sprint30_max"], reverse=True),
                "cmj": calculate_percentile(latest.get("cmj"), team_min["cmj_min"], team_max["cmj_max"]),
                "isrt": calculate_percentile(latest.get("isrt"), team_min["isrt_min"], team_max["isrt_max"]),
                "submax": calculate_percentile(latest.get("submax"), team_min["submax_min"], team_max["submax_max"]),
            }

    if player_id:
        tests = [r for r in test_rows if r["player_id"] == selected_player.id]
        tests.sort(key=lambda r: r["session_date"])
        anthropometry_dates = [t["session_date"].strftime("%d-%m-%Y") for t in tests]

        anthropometry_weights = []
        last_weight = None
        for t in tests:
            if t.get("curr_weight") is not None:
                last_weight = t.get("curr_weight")
            anthropometry_weights.append(last_weight)

        anthropometry_skinfolds = []
        last_skin = None
        for t in tests:
            if t.get("sum_skinfolds") is not None:
                last_skin = t.get("sum_skinfolds")
            anthropometry_skinfolds.append(last_skin)

    team_avg = {
        "sprint_10": round(mean(sprint10_vals), 2),
        "sprint_30": round(mean(sprint30_vals), 2),
        "cmj": round(mean(cmj_vals), 2),
        "isrt": round(mean(isrt_vals), 2),
        "submax": round(mean(submax_vals), 2),
    }

    if request.method == "POST":
        if _is_player_app_user(request.user):
            raise PermissionDenied
        player_obj = get_object_or_404(Player, id=request.POST.get("player_id"))
        test_date = request.POST.get("test_date")
        if not test_date:
            _record_data_import_log(
                request,
                data_type="Testdata",
                filename="Handmatige invoer",
                upload_selection={
                    "team_code": selected_team_code,
                    "team_label": selected_team_label,
                    "event_code": "testdata",
                    "event_label": "Testdata",
                },
                status="failed",
                error_count=1,
                details=[f"Testdata voor {player_obj.name} niet opgeslagen: datum ontbreekt."],
            )
            return redirect(f"/testdata/?tab=invoer&team={selected_team_code}")

        try:
            parsed_date = datetime.strptime(test_date, "%Y-%m-%d").date()
        except ValueError:
            _record_data_import_log(
                request,
                data_type="Testdata",
                filename="Handmatige invoer",
                upload_selection={
                    "team_code": selected_team_code,
                    "team_label": selected_team_label,
                    "event_code": "testdata",
                    "event_label": "Testdata",
                },
                status="failed",
                error_count=1,
                details=[f"Testdata voor {player_obj.name} niet opgeslagen: datum is ongeldig."],
            )
            messages.error(request, "Kies een geldige datum voor de testdata.")
            return redirect(f"/testdata/?tab=invoer&team={selected_team_code}")

        submitted_metrics = {
            "sprint_10": request.POST.get("sprint_10"),
            "sprint_30": request.POST.get("sprint_30"),
            "cmj": request.POST.get("cmj"),
            "isrt": request.POST.get("isrt"),
            "submax": request.POST.get("submax"),
            "curr_weight": request.POST.get("curr_weight"),
            "length": request.POST.get("length"),
            "sum_skinfolds": request.POST.get("sum_skinfolds"),
        }
        filled_metric_count = sum(1 for value in submitted_metrics.values() if str(value or "").strip())
        upsert_performance_session_metrics(
            player=player_obj,
            session_kind="test",
            session_date=parsed_date,
            metrics=submitted_metrics,
            source_tag="main_manual_test",
        )
        redirect_team_code = team_code_for_player(player_obj.id) or selected_team_code
        _record_data_import_log(
            request,
            data_type="Testdata",
            filename="Handmatige invoer",
            upload_selection={
                "team_code": redirect_team_code,
                "team_label": _academy_team_label(redirect_team_code),
                "event_code": "testdata",
                "event_label": "Testdata",
            },
            status="success" if filled_metric_count else "partial",
            processed_count=1 if filled_metric_count else 0,
            error_count=0 if filled_metric_count else 1,
            details=[
                f"Testdata opgeslagen voor {player_obj.name} op {parsed_date.strftime('%d-%m-%Y')}."
                if filled_metric_count
                else f"Testdata-invoer voor {player_obj.name} bevatte geen ingevulde meetwaarden."
            ],
        )
        return redirect(f"/testdata/?tab=invoer&team={redirect_team_code}")

    context = {
        "players": [selected_player] if player_only_mode and selected_player else players,
        "selected_player": selected_player,
        "testdata_team_options": [] if player_only_mode else _academy_data_team_options(),
        "selected_team_code": selected_team_code,
        "selected_team_label": selected_team_label,
        "test_data": test_data,
        "team_avg": team_avg,
        "percentiles": percentiles,
        "active_testdata_tab": tab_param,
        "team_profile_rows": [] if player_only_mode else team_profile_rows,
        "player_only_mode": player_only_mode,
    }

    if player_id:
        context.update(
            {
                "anthropometry_dates": anthropometry_dates,
                "anthropometry_weights": anthropometry_weights,
                "anthropometry_skinfolds": anthropometry_skinfolds,
            }
        )

    return render(request, "testdata.html", context)


def _academy_codes():
    return ["OUD", "O21", "O19", "O17", "O15", "O14", "O13", "O12"]


def _academy_data_codes():
    return ["O21", "O19", "O17", "O15", "O14", "O13", "O12"]


def _academy_team_label(team_code):
    return "Oud spelers" if (team_code or "").strip().upper() == "OUD" else (team_code or "").strip().upper()


def _academy_team_options():
    return [{"code": code, "label": _academy_team_label(code)} for code in _academy_codes()]


def _academy_data_team_options():
    return [{"code": code, "label": _academy_team_label(code)} for code in _academy_data_codes()]


def _attendance_team_codes():
    return ["O21", "O19", "O17", "O15"]


def _attendance_team_options():
    return [{"code": code, "label": _academy_team_label(code)} for code in _attendance_team_codes()]


def _academy_team_context(team_code):
    academy_codes = _academy_codes()
    requested_code = (team_code or "").strip().upper()
    if requested_code not in academy_codes:
        requested_code = "O21"

    team_obj = Team.objects.filter(
        Q(code__iexact=requested_code) | Q(name__iexact=requested_code),
        is_active=True,
    ).first()
    team_label = team_obj.name if team_obj else _academy_team_label(requested_code)

    players = Player.objects.select_related("position_ref", "monitoring_profile").none()
    if requested_code == "OUD":
        today = timezone.localdate()
        assigned_old_players = Player.objects.none()
        if team_obj:
            assigned_old_players = (
                Player.objects
                .select_related("position_ref", "monitoring_profile")
                .filter(team_assignments__team=team_obj)
                .filter(Q(team_assignments__end_date__isnull=True) | Q(team_assignments__end_date__gte=today))
            )
        players = (
            Player.objects
            .select_related("position_ref", "monitoring_profile")
            .filter(Q(is_active=False) | Q(id__in=assigned_old_players.values("id")))
            .distinct()
            .order_by("name")
        )
    elif team_obj:
        today = timezone.localdate()
        players = (
            Player.objects
            .select_related("position_ref", "monitoring_profile")
            .filter(
                is_active=True,
                team_assignments__team=team_obj,
            )
            .filter(Q(team_assignments__end_date__isnull=True) | Q(team_assignments__end_date__gte=today))
            .distinct()
            .order_by("name")
        )

    demo_players = False
    if requested_code == "O19" and not players.exists():
        players = Player.objects.select_related("position_ref", "monitoring_profile").filter(is_active=True).order_by("name")[:8]
        demo_players = True

    return {
        "academy_codes": academy_codes,
        "academy_team_options": _academy_team_options(),
        "requested_code": requested_code,
        "team_obj": team_obj,
        "team_label": team_label,
        "players": players,
        "demo_players": demo_players,
    }


def academie_team(request, team_code):
    import json

    academy_context = _academy_team_context(team_code)
    academy_codes = academy_context["academy_codes"]
    requested_code = academy_context["requested_code"]
    team_obj = academy_context["team_obj"]
    team_label = academy_context["team_label"]
    players = academy_context["players"]

    player_ids = set(players.values_list("id", flat=True))

    def team_rows(session_kind):
        return fetch_performance_rows(session_kind, player_ids=player_ids)

    training_rows = team_rows("training")
    match_rows = team_rows("match")
    test_rows = team_rows("test")

    latest_training_date = max((row["session_date"] for row in training_rows), default=None)
    gps_start_date = latest_training_date - timedelta(days=29) if latest_training_date else None
    recent_training_rows = [
        row for row in training_rows
        if gps_start_date is None or row["session_date"] >= gps_start_date
    ]

    def val(row, key):
        return float(row.get(key) or 0)

    gps_by_player = {}
    for row in recent_training_rows:
        data = gps_by_player.setdefault(
            row["player_id"],
            {
                "player": row["player_obj"],
                "load": 0.0,
                "total_distance": 0.0,
                "hsd": 0.0,
                "sprints": 0.0,
                "sessions": 0,
            },
        )
        data["load"] += val(row, "load")
        data["total_distance"] += val(row, "total_distance")
        data["hsd"] += val(row, "hsd")
        data["sprints"] += val(row, "sprints")
        data["sessions"] += 1

    gps_rows = sorted(gps_by_player.values(), key=lambda item: item["load"], reverse=True)
    gps_totals = {
        "load": sum(item["load"] for item in gps_rows),
        "distance": sum(item["total_distance"] for item in gps_rows),
        "hsd": sum(item["hsd"] for item in gps_rows),
        "sprints": sum(item["sprints"] for item in gps_rows),
    }

    latest_tests = {}
    for row in sorted(test_rows, key=lambda item: item["session_date"], reverse=True):
        latest_tests.setdefault(row["player_id"], row)

    latest_weights = {}
    for weight in WeightEntry.objects.filter(player_id__in=player_ids).select_related("player").order_by("player_id", "-date", "-id"):
        latest_weights.setdefault(weight.player_id, weight)

    latest_anthropometry = {}
    for session in (
        AnthropometrySession.objects
        .filter(player_id__in=player_ids)
        .select_related("player")
        .prefetch_related("measurements")
        .order_by("player_id", "-date", "-id")
    ):
        latest_anthropometry.setdefault(session.player_id, session)

    test_table_rows = [
    ]
    for player in players:
        row = latest_tests.get(player.id)
        weight_entry = latest_weights.get(player.id)
        anthropometry = latest_anthropometry.get(player.id)
        profile = getattr(player, "monitoring_profile", None)
        skinfold_sum = None
        if row and row.get("sum_skinfolds") is not None:
            skinfold_sum = row.get("sum_skinfolds")
        elif anthropometry:
            skinfold_values = [
                measurement.value
                for measurement in anthropometry.measurements.all()
                if measurement.category == "skinfold"
            ]
            skinfold_sum = sum(skinfold_values) if skinfold_values else None
        elif profile:
            skinfold_sum = profile.sum_skinfolds

        weight_value = None
        weight_date = None
        if weight_entry:
            weight_value = weight_entry.weight
            weight_date = weight_entry.date
        elif anthropometry and anthropometry.body_mass is not None:
            weight_value = anthropometry.body_mass
            weight_date = anthropometry.date
        elif row and row.get("curr_weight") is not None:
            weight_value = row.get("curr_weight")
            weight_date = row.get("session_date")
        elif profile:
            weight_value = profile.curr_weight

        fat_value = None
        if anthropometry and anthropometry.fat_average is not None:
            fat_value = anthropometry.fat_average
        elif profile:
            fat_value = profile.fat_perc

        has_speed = bool(row and any(row.get(code) is not None for code in ("sprint_10", "sprint_30", "cmj")))
        has_body = any(value is not None for value in (weight_value, skinfold_sum, fat_value))
        has_condition = bool(row and row.get("isrt") is not None)

        test_table_rows.append(
            {
                "player": player,
                "row": row,
                "test_url": f"{reverse('testdata')}?player_id={player.id}&tab=profiel",
                "test_date": row.get("session_date") if row else None,
                "weight_value": weight_value,
                "weight_date": weight_date,
                "skinfold_sum": skinfold_sum,
                "fat_value": fat_value,
                "anthropometry_date": anthropometry.date if anthropometry else None,
                "has_speed": has_speed,
                "has_body": has_body,
                "has_condition": has_condition,
                "complete_count": sum([has_speed, has_body, has_condition]),
            }
        )

    test_summary = {
        "speed": sum(1 for item in test_table_rows if item["has_speed"]),
        "body": sum(1 for item in test_table_rows if item["has_body"]),
        "condition": sum(1 for item in test_table_rows if item["has_condition"]),
        "complete": sum(1 for item in test_table_rows if item["complete_count"] >= 3),
    }
    test_metric_config = [
        ("sprint_10", "10 meter sprint", "sec"),
        ("sprint_30", "30 meter sprint", "sec"),
        ("cmj", "CMJ", "cm"),
        ("squat_jump", "Squat jump", "cm"),
        ("isrt", "ISRT", ""),
        ("weight_value", "Gewicht", "kg"),
        ("skinfold_sum", "Huidplooien", "mm"),
        ("fat_value", "Vetpercentage", "%"),
    ]
    test_chart_labels = [item["player"].name for item in test_table_rows]
    test_chart_data = {}
    for code, label, unit in test_metric_config:
        values = []
        dates = []
        for item in test_table_rows:
            if code in {"weight_value", "skinfold_sum", "fat_value"}:
                value = item.get(code)
                date_value = item.get("weight_date") or item.get("anthropometry_date")
            else:
                row = item.get("row") or {}
                value = row.get(code)
                date_value = item.get("test_date")
            values.append(round(float(value), 2) if value is not None else None)
            dates.append(date_value.strftime("%d-%m-%Y") if date_value else "-")
        test_chart_data[code] = {
            "label": label,
            "unit": unit,
            "values": values,
            "dates": dates,
        }

    latest_matches = {}
    for row in sorted(match_rows, key=lambda item: item["session_date"], reverse=True):
        latest_matches.setdefault(row["player_id"], row)
    match_table_rows = [
        {
            "player": player,
            "row": latest_matches.get(player.id),
        }
        for player in players
    ]
    match_totals = {
        "load": sum(val(row, "load") for row in match_rows),
        "distance": sum(val(row, "total_distance") for row in match_rows),
        "sprints": sum(val(row, "sprints") for row in match_rows),
        "matches": len(match_rows),
    }

    latest_wellness_date = (
        WellnessEntry.objects
        .filter(player_id__in=player_ids)
        .order_by("-date")
        .values_list("date", flat=True)
        .first()
    ) or timezone.localdate()
    wellness_entries = {
        entry.player_id: entry
        for entry in (
            WellnessEntry.objects
            .filter(player_id__in=player_ids, date=latest_wellness_date)
            .select_related("player")
        )
    }
    wellness_labels = _wellness_label_sets()
    wellness_rows = []
    wellness_scores = []
    for player in players:
        entry = wellness_entries.get(player.id)
        score = _wellness_score(entry)
        if score is not None:
            wellness_scores.append(score)
        wellness_rows.append(
            {
                "player": player,
                "entry": entry,
                "score": score,
                "status": "Ingevuld" if entry else "Niet ingevuld",
                "sleep_label": _wellness_label(entry.sleep if entry else None, wellness_labels["sleep"]),
                "mood_label": _wellness_label(entry.mood if entry else None, wellness_labels["mood"]),
                "fitness_label": _wellness_label(entry.fitness if entry else None, wellness_labels["fitness"]),
                "soreness_label": _wellness_label(entry.soreness if entry else None, wellness_labels["soreness"]),
            }
        )
    wellness_filled_count = sum(1 for item in wellness_rows if item["entry"])
    wellness_total_count = len(wellness_rows)
    wellness_summary = {
        "date": latest_wellness_date,
        "filled": wellness_filled_count,
        "missing": max(wellness_total_count - wellness_filled_count, 0),
        "total": wellness_total_count,
        "percentage": round((wellness_filled_count / wellness_total_count) * 100) if wellness_total_count else None,
        "average": round(sum(wellness_scores) / len(wellness_scores), 1) if wellness_scores else None,
    }

    active_injuries = (
        InjuryCase.objects
        .select_related("player", "injury_type_ref", "phase_ref", "status_ref")
        .filter(player_id__in=player_ids, closed_on__isnull=True)
        .order_by("expected_return_on", "started_on", "player__name")
    )
    rehab_rows = []
    for injury in active_injuries:
        ui = _injury_to_ui(injury)
        rehab_rows.append(
            {
                "injury": ui,
                "player_id": injury.player_id,
                "rehab_url": f"{reverse('revalidatie')}?team={requested_code}&player_id={injury.player_id}",
            }
        )
    rehab_summary = {
        "total": len(rehab_rows),
        "early": sum(1 for item in rehab_rows if item["injury"].phase == "early"),
        "mid": sum(1 for item in rehab_rows if item["injury"].phase == "mid"),
        "final": sum(1 for item in rehab_rows if item["injury"].phase == "final"),
    }

    context = {
        "academy_codes": academy_codes,
        "academy_team_options": academy_context["academy_team_options"],
        "selected_team_code": requested_code,
        "selected_team_label": team_label,
        "team_exists": team_obj is not None or requested_code == "OUD",
        "demo_players": academy_context["demo_players"],
        "players": players,
        "gps_rows": gps_rows,
        "gps_totals": gps_totals,
        "test_table_rows": test_table_rows,
        "test_summary": test_summary,
        "test_metric_config": test_metric_config,
        "test_chart_labels": json.dumps(test_chart_labels),
        "test_chart_data": json.dumps(test_chart_data),
        "match_table_rows": match_table_rows,
        "match_totals": match_totals,
        "wellness_rows": wellness_rows,
        "wellness_summary": wellness_summary,
        "rehab_rows": rehab_rows,
        "rehab_summary": rehab_summary,
        "gps_chart_labels": json.dumps([item["player"].name for item in gps_rows]),
        "gps_chart_load": json.dumps([round(item["load"], 1) for item in gps_rows]),
        "gps_chart_distance": json.dumps([round(item["total_distance"], 1) for item in gps_rows]),
        "match_chart_labels": json.dumps([item["player"].name for item in match_table_rows if item["row"]]),
        "match_chart_load": json.dumps([round(val(item["row"], "load"), 1) for item in match_table_rows if item["row"]]),
        "active_page": "academie",
    }
    return render(request, "academie_team.html", context)


def academie_player(request, team_code, player_id):
    academy_context = _academy_team_context(team_code)
    requested_code = academy_context["requested_code"]
    player_queryset = Player.objects.select_related("position_ref", "monitoring_profile")
    if requested_code != "OUD":
        player_queryset = player_queryset.filter(is_active=True)
    player = get_object_or_404(player_queryset, id=player_id)

    rows_training = [row for row in fetch_performance_rows("training") if row["player_id"] == player.id]
    rows_match = [row for row in fetch_performance_rows("match") if row["player_id"] == player.id]
    rows_test = [row for row in fetch_performance_rows("test") if row["player_id"] == player.id]

    latest_training_date = max((row["session_date"] for row in rows_training), default=None)
    gps_start = latest_training_date - timedelta(days=29) if latest_training_date else None
    recent_training = [row for row in rows_training if gps_start is None or row["session_date"] >= gps_start]

    def val(row, key):
        return float(row.get(key) or 0)

    gps_totals = {
        "load": sum(val(row, "load") for row in recent_training),
        "distance": sum(val(row, "total_distance") for row in recent_training),
        "hsd": sum(val(row, "hsd") for row in recent_training),
        "sprints": sum(val(row, "sprints") for row in recent_training),
        "sessions": len(recent_training),
    }
    match_totals = {
        "load": sum(val(row, "load") for row in rows_match),
        "distance": sum(val(row, "total_distance") for row in rows_match),
        "matches": len(rows_match),
    }

    performance_rows = [*rows_training, *rows_match]
    latest_session_date = max(
        (row.get("session_date") for row in performance_rows if row.get("session_date")),
        default=timezone.localdate(),
    )
    week_start = latest_session_date - timedelta(days=6)
    week_dates = [week_start + timedelta(days=index) for index in range(7)]
    previous_start = week_start - timedelta(days=21)
    current_week_rows = [
        row for row in performance_rows
        if row.get("session_date") and week_start <= row["session_date"] <= latest_session_date
    ]
    previous_rows = [
        row for row in performance_rows
        if row.get("session_date") and previous_start <= row["session_date"] < week_start
    ]
    chronic_daily_load = sum(val(row, "load") for row in previous_rows) / 21 if previous_rows else 0

    gps_labels = []
    gps_td_values = []
    gps_load_values = []
    gps_d15_values = []
    gps_d20_values = []
    gps_d25_values = []
    gps_sprints_values = []
    gps_acwr_values = []
    gps_week_rows = []
    day_names_short = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]

    for day in week_dates:
        day_rows = [row for row in current_week_rows if row.get("session_date") == day]
        total_distance = sum(val(row, "total_distance") for row in day_rows)
        load = sum(val(row, "load") for row in day_rows)
        d15 = sum(val(row, "hsd") for row in day_rows)
        d20 = d15
        d25 = sum(val(row, "his") for row in day_rows)
        sprints = sum(val(row, "sprints") for row in day_rows)
        acwr = round(load / chronic_daily_load, 2) if chronic_daily_load else 0
        day_label = f"{day_names_short[day.weekday()]} {day.strftime('%d-%m')}"

        gps_labels.append(day_label)
        gps_td_values.append(round(total_distance, 1))
        gps_load_values.append(round(load, 1))
        gps_d15_values.append(round(d15, 1))
        gps_d20_values.append(round(d20, 1))
        gps_d25_values.append(round(d25, 1))
        gps_sprints_values.append(round(sprints, 1))
        gps_acwr_values.append(acwr)
        gps_week_rows.append({
            "date": day,
            "label": day_label,
            "load": round(load, 0),
            "distance_km": round(total_distance / 1000, 2),
            "sprints": round(sprints, 0),
            "acwr": acwr,
        })

    latest_test = sorted(rows_test, key=lambda row: row["session_date"], reverse=True)[0] if rows_test else None
    recent_tests = sorted(rows_test, key=lambda row: row["session_date"], reverse=True)[:10]
    recent_training_rows = sorted(recent_training, key=lambda row: row["session_date"], reverse=True)[:12]
    recent_match_rows = sorted(rows_match, key=lambda row: row["session_date"], reverse=True)[:8]
    today = timezone.localdate()
    attendance_qs = (
        AttendanceRecord.objects
        .select_related("status")
        .filter(player=player, date__gte=today - timedelta(days=30))
    )
    attendance_total_count = attendance_qs.count()
    attendance_present_count = attendance_qs.filter(completed=True).count()
    attendance_percentage = round((attendance_present_count / attendance_total_count) * 100) if attendance_total_count else None
    attendance_rows = attendance_qs.order_by("-date")[:10]
    recent_plan_notes = (
        IndividualDayPlanNote.objects
        .select_related("plan", "note_type_ref")
        .filter(plan__player=player)
        .exclude(content="")
        .order_by("-plan__date", "note_type_ref__label")[:10]
    )
    mdo_action_points = MDOActionPoint.objects.filter(player=player).order_by("is_done", "deadline", "-created_at")[:10]
    latest_wellness = WellnessEntry.objects.filter(player=player).order_by("-date").first()
    latest_rpe = RPEEntry.objects.filter(player=player).order_by("-date").first()

    context = {
        "academy_codes": academy_context["academy_codes"],
        "academy_team_options": academy_context["academy_team_options"],
        "selected_team_code": requested_code,
        "selected_team_label": academy_context["team_label"],
        "players": academy_context["players"],
        "demo_players": academy_context["demo_players"],
        "player": player,
        "gps_totals": gps_totals,
        "match_totals": match_totals,
        "latest_test": latest_test,
        "recent_tests": recent_tests,
        "recent_training_rows": recent_training_rows,
        "recent_match_rows": recent_match_rows,
        "gps_week_rows": gps_week_rows,
        "gps_labels": gps_labels,
        "gps_td_values": gps_td_values,
        "gps_load_values": gps_load_values,
        "gps_d15_values": gps_d15_values,
        "gps_d20_values": gps_d20_values,
        "gps_d25_values": gps_d25_values,
        "gps_sprints_values": gps_sprints_values,
        "gps_acwr_values": gps_acwr_values,
        "attendance_rows": attendance_rows,
        "attendance_total_count": attendance_total_count,
        "attendance_present_count": attendance_present_count,
        "attendance_percentage": attendance_percentage,
        "recent_plan_notes": recent_plan_notes,
        "mdo_action_points": mdo_action_points,
        "latest_wellness": latest_wellness,
        "latest_wellness_score": _wellness_score(latest_wellness),
        "latest_rpe": latest_rpe,
        "test_url": f"{reverse('testdata')}?player_id={player.id}&tab=profiel",
        "presence_url": f"{reverse('aanwezigheden')}?player_id={player.id}",
        "individual_url": f"{reverse('individuele_programmas')}?player_id={player.id}",
        "active_page": "academie",
    }
    return render(request, "academie_player.html", context)


# ---------- PAGINA: HERSTEL ----------
def recovery(request):
    """Pagina voor herstel- en testanalyse per speler."""
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")
    selected_player_name = request.GET.get("player")
    selected_player, recovery_data, chart_labels, chart_values = None, [], [], []

    if selected_player_name:
        selected_player = Player.objects.filter(name=selected_player_name).first()
        if selected_player:
            recovery_data = [
                {"name": "Sprint 10m", "date": "2025-09-01", "value": 1.74},
                {"name": "Sprint 30m", "date": "2025-09-01", "value": 4.32},
                {"name": "ISRT", "date": "2025-09-15", "value": 1940},
                {"name": "CMJ", "date": "2025-10-01", "value": 42.5},
                {"name": "Squat jump", "date": "2025-10-15", "value": 38.7},
            ]
            chart_labels = [r["name"] for r in recovery_data]
            chart_values = [float(r["value"]) for r in recovery_data]

    return render(
        request,
        "recovery.html",
        {"players": players, "selected_player": selected_player,
         "recovery_data": recovery_data, "chart_labels": chart_labels,
         "chart_values": chart_values},
    )


from django.shortcuts import render, redirect
from django.db.models import Sum
from datetime import timedelta
import json
from .models import (
    InjuryCase,
    Player,
    FieldRehabSession,
    FieldRehabPhase,
    FieldRehabComponent,
    FieldRehabMetric,
    FieldRehabMetricType,
)


def revalidatie(request):
    """Pagina voor overzicht van geblesseerde spelers + invoer van veldrevalidatie."""
    data_team_codes = _academy_data_codes()
    selected_player_id = request.GET.get("player_id")
    selected_player_name = request.GET.get("player")
    selected_player = None

    def team_code_for_player(player_id_value):
        if not player_id_value:
            return ""
        today = timezone.localdate()
        assignment = (
            PlayerTeamAssignment.objects
            .select_related("team")
            .filter(
                player_id=player_id_value,
                team__code__in=data_team_codes,
                start_date__lte=today,
            )
            .filter(Q(end_date__isnull=True) | Q(end_date__gte=today))
            .order_by("-start_date", "-id")
            .first()
        )
        return assignment.team.code if assignment and assignment.team else ""

    selected_team_code = (
        request.GET.get("team")
        or request.POST.get("team")
        or team_code_for_player(selected_player_id)
        or data_team_codes[0]
    ).strip().upper()
    if selected_team_code not in data_team_codes:
        selected_team_code = data_team_codes[0]
    selected_team, team_players_qs = _team_players_for_gps_upload(selected_team_code)
    selected_team_label = selected_team.name if selected_team else _academy_team_label(selected_team_code)
    players = list(team_players_qs.select_related("monitoring_profile", "position_ref"))
    team_player_ids = {player.id for player in players}
    injuries = (
        InjuryCase.objects
        .select_related("player", "injury_type_ref", "phase_ref", "status_ref")
        .filter(player_id__in=team_player_ids)
        .order_by("started_on")
    )

    if selected_player_id:
        selected_player = Player.objects.filter(id=selected_player_id).first()
    elif selected_player_name:
        # Backward compatibility voor bestaande links op naam.
        selected_player = Player.objects.filter(name=selected_player_name).first()

    if selected_player:
        injuries = InjuryCase.objects.select_related(
            "player", "injury_type_ref", "phase_ref", "status_ref"
        ).filter(player=selected_player).order_by("started_on")
    elif selected_player_id or selected_player_name:
        injuries = []

    # Default duur voor opbouwplanner (in dagen), afgeleid uit blessureduur indien mogelijk.
    rehab_duration_default_days = 28
    if selected_player:
        latest_with_duration = None
        for injury_item in injuries.order_by("-started_on"):
            if _injury_duration_days(injury_item) is not None:
                latest_with_duration = injury_item
                break
        if latest_with_duration and _injury_duration_days(latest_with_duration) is not None:
            try:
                duration_days = int(_injury_duration_days(latest_with_duration))
                rehab_duration_default_days = max(7, min(168, duration_days))
            except (TypeError, ValueError):
                rehab_duration_default_days = 28

    # Laatste 30 dagen trainingsdata voor geselecteerde speler (overzicht + ACWR)
    rehab_month_data = []
    rehab_month_labels = []
    rehab_month_loads = []
    rehab_month_distances = []
    rehab_month_hsd = []
    rehab_month_d20 = []
    rehab_month_d25 = []
    rehab_month_acc = []
    rehab_month_dec = []
    rehab_month_max_speed = []
    rehab_month_sprints = []
    rehab_month_acwr = []
    rehab_month_range_label = "-"

    if selected_player:
        player_training_rows = [
            r for r in fetch_performance_rows("training") if r["player_id"] == selected_player.id
        ]
        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=29)
        rehab_month_range_label = f"{start_date.strftime('%d-%m-%Y')} t/m {end_date.strftime('%d-%m-%Y')}"

        daily_map = {}
        for row in player_training_rows:
            current_date = row["session_date"]
            if current_date < start_date or current_date > end_date:
                continue
            agg = daily_map.setdefault(
                current_date,
                {"load": 0.0, "total_distance": 0.0, "hsd": 0.0, "sprints": 0.0},
            )
            agg["load"] += float(row.get("load") or 0)
            agg["total_distance"] += float(row.get("total_distance") or 0)
            agg["hsd"] += float(row.get("hsd") or 0)
            agg["sprints"] += float(row.get("sprints") or 0)
        day_name_short = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
        daily_load_values = []

        for day_offset in range(30):
            current_date = start_date + timedelta(days=day_offset)
            row = daily_map.get(current_date, {})

            day_load = float(row.get("load") or 0)
            day_total_distance = float(row.get("total_distance") or 0)
            day_hsd = float(row.get("hsd") or 0)
            day_sprints = float(row.get("sprints") or 0)

            rehab_month_labels.append(
                f"{day_name_short[current_date.weekday()]} {current_date.strftime('%d-%m')}"
            )
            rehab_month_loads.append(day_load)
            rehab_month_distances.append(day_total_distance)
            rehab_month_hsd.append(day_hsd)
            rehab_month_d20.append(day_hsd)   # alias in trainingsdata
            rehab_month_d25.append(0.0)       # niet beschikbaar in TrainingData
            rehab_month_acc.append(0.0)       # niet beschikbaar in TrainingData
            rehab_month_dec.append(0.0)       # niet beschikbaar in TrainingData
            rehab_month_max_speed.append(0.0) # niet beschikbaar in TrainingData
            rehab_month_sprints.append(day_sprints)
            daily_load_values.append(day_load)
            rehab_month_data.append(
                {
                    "date_label": current_date.strftime("%d-%m-%Y"),
                    "load": round(day_load, 1),
                    "total_distance": round(day_total_distance, 1),
                    "hsd": round(day_hsd, 1),
                    "d20": round(day_hsd, 1),   # alias in trainingsdata
                    "d25": 0.0,                 # niet beschikbaar in TrainingData
                    "acc": 0.0,                 # niet beschikbaar in TrainingData
                    "dec": 0.0,                 # niet beschikbaar in TrainingData
                    "max_speed": 0.0,           # niet beschikbaar in TrainingData
                    "sprints": round(day_sprints, 1),
                    "acwr": None,
                }
            )

        # EWMA-7 / EWMA-28 en ACWR op dagbasis
        lambda_acute = 2 / 8
        lambda_chronic = 2 / 29
        acute_ewma = []
        chronic_ewma = []

        for idx, val in enumerate(daily_load_values):
            if idx == 0:
                acute_val = val
                chronic_val = val
            else:
                acute_val = (lambda_acute * val) + ((1 - lambda_acute) * acute_ewma[idx - 1])
                chronic_val = (lambda_chronic * val) + ((1 - lambda_chronic) * chronic_ewma[idx - 1])
            acute_ewma.append(acute_val)
            chronic_ewma.append(chronic_val)

        for idx in range(len(daily_load_values)):
            chronic_val = chronic_ewma[idx]
            acwr_val = round(acute_ewma[idx] / chronic_val, 2) if chronic_val > 0 else None
            rehab_month_acwr.append(acwr_val)
            rehab_month_data[idx]["acwr"] = acwr_val

    if request.GET.get("ajax") == "1":
        injuries_payload = []
        for injury in injuries:
            phase = injury.phase_ref.code if injury.phase_ref else ""
            if phase == "early":
                phase_label = "Vroege fase"
            elif phase == "mid":
                phase_label = "Middenfase"
            else:
                phase_label = "Laatste fase"

            injuries_payload.append(
                {
                    "name": injury.player.name,
                    "injury_type": injury.injury_type_ref.name if injury.injury_type_ref else "-",
                    "start_date": injury.started_on.strftime("%d-%m-%Y") if injury.started_on else "-",
                    "duration": _injury_duration_days(injury) or "-",
                    "phase": phase,
                    "phase_label": phase_label,
                }
            )

        return JsonResponse(
            {
                "selected_player": {
                    "id": selected_player.id if selected_player else None,
                    "name": selected_player.name if selected_player else "",
                },
                "injuries": injuries_payload,
                "rehab_month_range_label": rehab_month_range_label,
                "rehab_month_data": rehab_month_data,
                "rehab_month_labels": rehab_month_labels,
                "rehab_month_loads": rehab_month_loads,
                "rehab_month_distances": rehab_month_distances,
                "rehab_month_hsd": rehab_month_hsd,
                "rehab_month_d20": rehab_month_d20,
                "rehab_month_d25": rehab_month_d25,
                "rehab_month_acc": rehab_month_acc,
                "rehab_month_dec": rehab_month_dec,
                "rehab_month_max_speed": rehab_month_max_speed,
                "rehab_month_sprints": rehab_month_sprints,
                "rehab_month_acwr": rehab_month_acwr,
                "rehab_duration_default_days": rehab_duration_default_days,
                "rehab_duration_default_weeks": max(1, min(24, (rehab_duration_default_days + 6) // 7)),
            }
        )

    # Formulierverwerking
    if request.method == "POST":
        if request.POST.get("form_type") == "add_injury_field":
            player_id = request.POST.get("injury_player")
            injury_type = request.POST.get("injury_type")
            start_date = request.POST.get("start_date")
            expected_return = request.POST.get("expected_return")
            phase = request.POST.get("injury_phase")

            if not player_id or not injury_type or not start_date or not expected_return or not phase:
                messages.error(request, "Vul speler, type blessure, startdatum, verwachte terugkeer en fase in.")
                return redirect(f"{reverse('revalidatie')}?team={selected_team_code}")

            try:
                player = Player.objects.get(id=player_id)
            except Player.DoesNotExist:
                messages.error(request, "Ongeldige speler geselecteerd.")
                return redirect(f"{reverse('revalidatie')}?team={selected_team_code}")

            _upsert_injury_case(
                player=player,
                injury_type=injury_type,
                start_date_value=start_date,
                duration_value=None,
                expected_return_value=expected_return,
                phase=phase,
            )
            messages.success(request, f"Blessure voor {player.name} toegevoegd.")
            redirect_team_code = team_code_for_player(player.id) or selected_team_code
            return redirect(f"{reverse('revalidatie')}?team={redirect_team_code}")

        player_id = request.POST.get("player")
        phase = request.POST.get("phase")

        onderdelen = request.POST.getlist("onderdeel[]")
        duuren = request.POST.getlist("duur[]")
        rpes = request.POST.getlist("rpe[]")
        totale_afstanden = request.POST.getlist("totale_afstand[]")
        afstand_20s = request.POST.getlist("afstand_20[]")
        afstand_25s = request.POST.getlist("afstand_25[]")
        acceleraties = request.POST.getlist("acceleraties[]")
        deceleraties = request.POST.getlist("deceleraties[]")
        afgevinkts = request.POST.getlist("afgevinkt[]")

        try:
            player = Player.objects.get(id=player_id)
            for i in range(len(onderdelen)):
                onderdeel = onderdelen[i].strip() if onderdelen[i] else None
                if not onderdeel:
                    continue

                phase_obj = None
                if phase:
                    phase_obj, _ = FieldRehabPhase.objects.get_or_create(name=phase.strip())

                onderdeel_obj, _ = FieldRehabComponent.objects.get_or_create(name=onderdeel)

                session = FieldRehabSession(
                    player=player,
                    phase_ref=phase_obj,
                    onderdeel_ref=onderdeel_obj,
                    afgevinkt=True if i < len(afgevinkts) and afgevinkts[i] == "on" else False,
                )
                session.save()

                metric_inputs = {
                    "duur": duuren[i] if i < len(duuren) else None,
                    "rpe": rpes[i] if i < len(rpes) else None,
                    "totale_afstand": totale_afstanden[i] if i < len(totale_afstanden) else None,
                    "afstand_20": afstand_20s[i] if i < len(afstand_20s) else None,
                    "afstand_25": afstand_25s[i] if i < len(afstand_25s) else None,
                    "acceleraties": acceleraties[i] if i < len(acceleraties) else None,
                    "deceleraties": deceleraties[i] if i < len(deceleraties) else None,
                }
                for code, raw_value in metric_inputs.items():
                    if raw_value in (None, ""):
                        continue
                    try:
                        metric_value = int(float(str(raw_value).replace(",", ".")))
                    except (TypeError, ValueError):
                        continue
                    metric_type, _ = FieldRehabMetricType.objects.get_or_create(
                        code=code,
                        defaults={"name": code.replace("_", " ").title()},
                    )
                    FieldRehabMetric.objects.update_or_create(
                        session=session,
                        metric_type=metric_type,
                        defaults={"value": metric_value},
                    )
        except Player.DoesNotExist:
            print("Ongeldige speler geselecteerd")

        if player_id:
            redirect_team_code = team_code_for_player(player_id) or selected_team_code
            return redirect(f"{reverse('revalidatie')}?team={redirect_team_code}&player_id={player_id}")
        if selected_player:
            redirect_team_code = team_code_for_player(selected_player.id) or selected_team_code
            return redirect(f"{reverse('revalidatie')}?team={redirect_team_code}&player_id={selected_player.id}")
        return redirect(f"{reverse('revalidatie')}?team={selected_team_code}")

    context = {
        "injuries": [_injury_to_ui(injury) for injury in injuries],
        "players": players,
        "selected_player": selected_player,
        "rehab_team_options": _academy_data_team_options(),
        "selected_team_code": selected_team_code,
        "selected_team_label": selected_team_label,
        "rehab_month_data": rehab_month_data,
        "rehab_month_range_label": rehab_month_range_label,
        "rehab_month_labels_json": json.dumps(rehab_month_labels),
        "rehab_month_data_json": json.dumps(rehab_month_data),
        "rehab_month_loads_json": json.dumps(rehab_month_loads),
        "rehab_month_distances_json": json.dumps(rehab_month_distances),
        "rehab_month_hsd_json": json.dumps(rehab_month_hsd),
        "rehab_month_d20_json": json.dumps(rehab_month_d20),
        "rehab_month_d25_json": json.dumps(rehab_month_d25),
        "rehab_month_acc_json": json.dumps(rehab_month_acc),
        "rehab_month_dec_json": json.dumps(rehab_month_dec),
        "rehab_month_max_speed_json": json.dumps(rehab_month_max_speed),
        "rehab_month_sprints_json": json.dumps(rehab_month_sprints),
        "rehab_month_acwr_json": json.dumps(rehab_month_acwr),
        "rehab_duration_default_days": rehab_duration_default_days,
        "rehab_duration_default_weeks": max(1, min(24, (rehab_duration_default_days + 6) // 7)),
    }

    return render(request, "revalidatie.html", context)
def revalidatie_gym(request):
    """Pagina voor oefeningen en voortgang in de revalidatiegym."""
    kracht_label = "Krachtprogramma"
    offfeet_label = "Conditionering off-feet"
    if request.method == "POST":
        if request.POST.get("form_type") == "add_injury_gym":
            player_id = request.POST.get("injury_player")
            name = request.POST.get("name")
            injury_type = request.POST.get("injury_type")
            start_date = request.POST.get("start_date")
            duration = request.POST.get("duration")
            expected_return = request.POST.get("expected_return")
            phase = request.POST.get("phase")

            if not injury_type or not start_date or not phase or not (duration or expected_return):
                messages.error(request, "Vul speler, blessuretype, startdatum, terugkeer en fase in.")
                return redirect("revalidatie_gym")

            player_obj = None
            if player_id:
                try:
                    player_obj = Player.objects.get(id=int(player_id))
                except (Player.DoesNotExist, ValueError, TypeError):
                    player_obj = None
            if player_obj is None:
                player_obj = _resolve_player_by_name(name)
            if player_obj is None:
                messages.error(request, "Speler niet gevonden. Voeg eerst de speler toe.")
                return redirect("revalidatie_gym")

            _upsert_injury_case(
                player=player_obj,
                injury_type=injury_type,
                start_date_value=start_date,
                duration_value=duration,
                expected_return_value=expected_return,
                phase=phase,
            )

            messages.success(request, f"Blessure van {player_obj.name} toegevoegd.")
            return redirect("revalidatie_gym")

        if request.POST.get("form_type") == "edit_injury_gym":
            injury_id = request.POST.get("injury_id")
            injury = get_object_or_404(InjuryCase, id=injury_id)

            name = request.POST.get("name")
            injury_type = request.POST.get("injury_type")
            start_date = request.POST.get("start_date")
            duration = request.POST.get("duration")
            phase = request.POST.get("phase")

            if not name or not injury_type or not start_date or not duration or not phase:
                messages.error(request, "Alle velden voor blessure bewerken zijn verplicht.")
                return redirect("revalidatie_gym")

            player_obj = _resolve_player_by_name(name)
            if player_obj is None:
                messages.error(request, "Speler niet gevonden. Voeg eerst de speler toe.")
                return redirect("revalidatie_gym")

            _upsert_injury_case(
                player=player_obj,
                injury_type=injury_type,
                start_date_value=start_date,
                duration_value=duration,
                phase=phase,
                instance=injury,
            )

            messages.success(request, "Blessure aangepast.")
            return redirect("revalidatie_gym")

        player = request.POST.get("player")
        program_type = request.POST.get("program_type", "").strip()
        phase = request.POST.get("phase")
        focus_point = request.POST.get("focus_point")
        exercise = request.POST.get("exercise")
        description = request.POST.get("description")
        sets_reps = request.POST.get("sets_reps")

        if not player or not phase or not exercise:
            messages.error(request, "Speler, fase en oefening zijn verplicht.")
            return redirect("revalidatie_gym")

        if program_type not in {kracht_label, offfeet_label}:
            program_type = kracht_label

        full_phase = f"{program_type} | {phase}"

        # Eerst proberen de juiste speler op te halen op basis van ID
        try:
            player_obj = Player.objects.get(id=int(player))
        except (Player.DoesNotExist, ValueError, TypeError):
            player_obj = None

        # Dan de oefening aanmaken met de juiste ForeignKey
        Oefening.objects.create(
            player=player_obj,
            phase=full_phase,
            focus_point=focus_point,
            exercise=exercise,
            description=description,
            sets_reps=sets_reps
        )

        return redirect("revalidatie_gym")

    oefeningen = Oefening.objects.select_related(
        "player", "program_type_ref", "phase_ref", "focus_point_ref"
    ).order_by("-created_at")
    oefeningen_kracht = oefeningen.filter(program_type_ref__name=kracht_label)
    oefeningen_offfeet = oefeningen.filter(program_type_ref__name=offfeet_label)
    spelers = Player.objects.all().order_by("name")
    blessures = InjuryCase.objects.select_related(
        "player", "injury_type_ref", "phase_ref", "status_ref"
    ).order_by("-started_on")

    today = date.today()

    return render(request, "revalidatie_gym.html", {
        "oefeningen": oefeningen,
        "oefeningen_kracht": oefeningen_kracht,
        "oefeningen_offfeet": oefeningen_offfeet,
        "kracht_label": kracht_label,
        "offfeet_label": offfeet_label,
        "spelers": spelers,
        "blessures": [_injury_to_ui(injury) for injury in blessures],
        "today": today,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date

from .models import (
    AnthropometrySession,
    AttendanceRecord,
    AttendanceStatus,
    IndividualDayPlan,
    IndividualDayPlanNote,
    IndividualDayPlanNoteType,
    MDOActionPoint,
    OverigNote,
    Player,
    Programma,
    ProgrammaDuurUnit,
    ProgrammaFrequentie,
    ProgrammaOefening,
    ProgrammaOefeningNaam,
    RPEEntry,
    WellnessEntry,
    WeightEntry,
)

# -------------------------------------
# PAGINA: individuele_programmas
# -------------------------------------
def individuele_programmas(request):
    """
    Pagina waar:
    - een speler geselecteerd kan worden
    - dagprogramma (DailyProgram) kan worden bekeken & opgeslagen
    - laatste individuele programma + oefeningen worden getoond
    """

    # Haal geselecteerde speler uit URL parameters
    player_id = request.GET.get("player_id")
    active_view = (request.GET.get("view") or request.POST.get("view") or "dagprogramma").strip().lower()
    if active_view not in {"dagprogramma", "trainen", "mdo"}:
        active_view = "dagprogramma"
    focus_tab = (request.GET.get("focus_tab") or "sprint-acceleratie").strip().lower()
    focus_tab_options = {
        "sprint-acceleratie": "Sprintacceleratie en houding",
        "hip-lock": "Hip Lock & Footplant",
        "core-control": "Core Control & Armcontrole",
        "cod": "CoD - remmen, houding en heraccelereren",
        "specifieke-hip-lock-cod": "Specifieke Hip Lock CoD-vorm",
    }
    if focus_tab not in focus_tab_options:
        focus_tab = "sprint-acceleratie"

    def team_code_for_player(player_id_value):
        if not player_id_value:
            return ""
        today = timezone.localdate()
        assignment = (
            PlayerTeamAssignment.objects
            .select_related("team")
            .filter(player_id=player_id_value, start_date__lte=today)
            .filter(Q(end_date__isnull=True) | Q(end_date__gte=today))
            .order_by("-start_date", "-id")
            .first()
        )
        return assignment.team.code if assignment and assignment.team else ""

    selected_team_code = (
        request.GET.get("team")
        or request.POST.get("team")
        or team_code_for_player(player_id)
        or "O21"
    ).strip().upper()
    academy_context = _academy_team_context(selected_team_code)
    selected_team_code = academy_context["requested_code"]
    selected_team_label = academy_context["team_label"]
    players = academy_context["players"]
    selected_team_obj = SimpleNamespace(name=selected_team_label, code=selected_team_code)

    selected_player = None
    programma = None
    oefeningen = []
    day_program = None
    video_previews = []
    mdo_context = {
        "mdo_notes": [],
        "mdo_action_points": [],
        "mdo_open_action_count": 0,
        "mdo_overdue_action_count": 0,
        "player_profile_overview": {},
        "mdo_week_rows": [],
        "mdo_wellness_rows": [],
        "mdo_kpis": {
            "load": 0,
            "distance_km": 0,
            "sprints": 0,
            "avg_wellness": None,
            "avg_rpe": None,
        },
        "mdo_labels_json": "[]",
        "mdo_td_json": "[]",
        "mdo_load_json": "[]",
        "mdo_d15_json": "[]",
        "mdo_d20_json": "[]",
        "mdo_d25_json": "[]",
        "mdo_sprints_json": "[]",
        "mdo_acwr_json": "[]",
    }

    def _build_video_preview(raw_url):
        raw_url = (raw_url or "").strip()
        if not raw_url:
            return None

        parsed = urlparse(raw_url)
        host = (parsed.netloc or "").lower()
        path = parsed.path or ""

        if "youtube.com" in host:
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return {"url": raw_url, "embed_url": f"https://www.youtube.com/embed/{video_id}"}
        if "youtu.be" in host:
            video_id = path.strip("/")
            if video_id:
                return {"url": raw_url, "embed_url": f"https://www.youtube.com/embed/{video_id}"}
        if "vimeo.com" in host:
            video_id = path.strip("/").split("/")[-1]
            if video_id.isdigit():
                return {"url": raw_url, "embed_url": f"https://player.vimeo.com/video/{video_id}"}
        if "loom.com" in host and "/share/" in path:
            video_id = path.split("/share/")[-1].strip("/")
            if video_id:
                return {"url": raw_url, "embed_url": f"https://www.loom.com/embed/{video_id}"}
        if raw_url.lower().endswith((".mp4", ".webm", ".ogg")):
            return {"url": raw_url, "embed_url": raw_url, "is_direct_video": True}

        return {"url": raw_url, "embed_url": None}

    if player_id:
        selected_player = get_object_or_404(Player.objects.select_related("monitoring_profile", "position_ref"), id=player_id)

        # Dagprogramma ophalen of aanmaken (3NF: plan + note)
        plan, _ = IndividualDayPlan.objects.get_or_create(
            player=selected_player,
            date=date.today(),
        )
        note_type_obj, _ = IndividualDayPlanNoteType.objects.get_or_create(
            code="program_text",
            defaults={"label": "Programma tekst"},
        )
        note, _ = IndividualDayPlanNote.objects.get_or_create(
            plan=plan,
            note_type_ref=note_type_obj,
            defaults={"content": ""},
        )
        remarks_type_obj, _ = IndividualDayPlanNoteType.objects.get_or_create(
            code="remarks",
            defaults={"label": "Opmerkingen"},
        )
        remarks_note, _ = IndividualDayPlanNote.objects.get_or_create(
            plan=plan,
            note_type_ref=remarks_type_obj,
            defaults={"content": ""},
        )
        focus_area_type_obj, _ = IndividualDayPlanNoteType.objects.get_or_create(
            code="focus_area",
            defaults={"label": "Aandachtspunt tab"},
        )
        focus_area_note, _ = IndividualDayPlanNote.objects.get_or_create(
            plan=plan,
            note_type_ref=focus_area_type_obj,
            defaults={"content": ""},
        )
        focus_note_type_obj, _ = IndividualDayPlanNoteType.objects.get_or_create(
            code="focus_note",
            defaults={"label": "Aandachtspunt notitie"},
        )
        focus_note, _ = IndividualDayPlanNote.objects.get_or_create(
            plan=plan,
            note_type_ref=focus_note_type_obj,
            defaults={"content": ""},
        )
        saved_focus_tab = (focus_area_note.content or "").strip().lower()
        if saved_focus_tab in focus_tab_options and "focus_tab" not in request.GET:
            focus_tab = saved_focus_tab
        day_program = SimpleNamespace(
            date=plan.date,
            program_text=note.content,
            opmerkingen=remarks_note.content,
            focus_tab=focus_tab,
            focus_note=focus_note.content,
        )

        # Laatste individuele programma ophalen
        programma = Programma.objects.filter(player=selected_player).order_by("-created_at").first()

        if programma:
            oefeningen = ProgrammaOefening.objects.select_related(
                "naam_ref", "frequentie_ref", "duur_unit_ref"
            ).filter(programma=programma)
            video_previews = [
                preview
                for preview in (
                    _build_video_preview(line)
                    for line in (programma.video_links or "").splitlines()
                )
                if preview
            ]

        # Opslaan dagprogramma
        if request.method == "POST":
            if "save_remarks" in request.POST:
                remarks_note.content = request.POST.get("remarks_text", "")
                remarks_note.save(update_fields=["content", "updated_at"])
                messages.success(request, "Opmerkingen opgeslagen!")
            elif "save_program" in request.POST:
                note.content = request.POST.get("program_text", "")
                note.save(update_fields=["content", "updated_at"])
                messages.success(request, "Dagprogramma opgeslagen!")
            elif "save_focus_note" in request.POST:
                posted_focus_tab = (request.POST.get("focus_tab") or focus_tab).strip().lower()
                if posted_focus_tab not in focus_tab_options:
                    posted_focus_tab = focus_tab
                focus_area_note.content = posted_focus_tab
                focus_area_note.save(update_fields=["content", "updated_at"])
                focus_note.content = request.POST.get("focus_note", "")
                focus_note.save(update_fields=["content", "updated_at"])
                messages.success(request, "Aandachtspunt opgeslagen!")
                focus_tab = posted_focus_tab
            elif "save_mdo_note" in request.POST:
                note_text = (request.POST.get("mdo_note") or "").strip()
                if note_text:
                    OverigNote.objects.create(
                        note_type="note",
                        page_key="mdo",
                        section_key=f"player:{selected_player.id}",
                        text=note_text,
                    )
                    messages.success(request, "MDO-opmerking opgeslagen.")
                else:
                    messages.error(request, "Vul eerst een opmerking in.")
                active_view = "mdo"
            elif "save_mdo_action" in request.POST:
                action_title = (request.POST.get("mdo_action_title") or "").strip()
                action_owner = (request.POST.get("mdo_action_owner") or "").strip()
                action_status = (request.POST.get("mdo_action_status") or "orange").strip().lower()
                if action_status not in {"green", "orange", "red"}:
                    action_status = "orange"
                action_deadline = parse_date(request.POST.get("mdo_action_deadline") or "")
                if action_title:
                    MDOActionPoint.objects.create(
                        player=selected_player,
                        title=action_title,
                        owner=action_owner,
                        deadline=action_deadline,
                        status_color=action_status,
                    )
                    messages.success(request, "MDO-actiepunt opgeslagen.")
                else:
                    messages.error(request, "Vul eerst een actiepunt in.")
                active_view = "mdo"
            elif "complete_mdo_action" in request.POST:
                action_id = request.POST.get("action_id")
                action = MDOActionPoint.objects.filter(player=selected_player, id=action_id).first()
                if action:
                    action.is_done = True
                    action.save(update_fields=["is_done", "updated_at"])
                    messages.success(request, "Actiepunt afgerond.")
                active_view = "mdo"
            return redirect(f"/individuele_programmas/?team={selected_team_code}&player_id={player_id}&focus_tab={focus_tab}&view={active_view}")

        today = date.today()
        player_training_rows = fetch_performance_rows("training", selected_player)
        player_match_rows = fetch_performance_rows("match", selected_player)
        performance_rows = [*player_training_rows, *player_match_rows]
        latest_session_date = max(
            (row.get("session_date") for row in performance_rows if row.get("session_date")),
            default=today,
        )
        week_start = latest_session_date - timedelta(days=6)
        week_dates = [week_start + timedelta(days=index) for index in range(7)]
        previous_start = week_start - timedelta(days=21)

        def _row_value(row, key):
            try:
                return float(row.get(key) or 0)
            except (TypeError, ValueError):
                return 0.0

        current_week_rows = [
            row for row in performance_rows
            if row.get("session_date") and week_start <= row["session_date"] <= latest_session_date
        ]
        previous_rows = [
            row for row in performance_rows
            if row.get("session_date") and previous_start <= row["session_date"] < week_start
        ]
        chronic_daily_load = sum(_row_value(row, "load") for row in previous_rows) / 21 if previous_rows else 0

        mdo_labels = []
        mdo_td_values = []
        mdo_load_values = []
        mdo_d15_values = []
        mdo_d20_values = []
        mdo_d25_values = []
        mdo_sprints_values = []
        mdo_acwr_values = []
        mdo_week_rows = []
        day_names_short = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]

        for day in week_dates:
            day_rows = [row for row in current_week_rows if row.get("session_date") == day]
            total_distance = sum(_row_value(row, "total_distance") for row in day_rows)
            load = sum(_row_value(row, "load") for row in day_rows)
            d15 = sum(_row_value(row, "hsd") for row in day_rows)
            d20 = d15
            d25 = sum(_row_value(row, "his") for row in day_rows)
            sprints = sum(_row_value(row, "sprints") for row in day_rows)
            acwr = round((load / chronic_daily_load), 2) if chronic_daily_load else 0
            day_label = f"{day_names_short[day.weekday()]} {day.strftime('%d-%m')}"
            mdo_labels.append(day_label)
            mdo_td_values.append(round(total_distance, 1))
            mdo_load_values.append(round(load, 1))
            mdo_d15_values.append(round(d15, 1))
            mdo_d20_values.append(round(d20, 1))
            mdo_d25_values.append(round(d25, 1))
            mdo_sprints_values.append(round(sprints, 1))
            mdo_acwr_values.append(acwr)
            mdo_week_rows.append({
                "date": day,
                "label": day_label,
                "distance_km": round(total_distance / 1000, 2),
                "load": round(load, 0),
                "sprints": round(sprints, 0),
                "acwr": acwr,
            })

        wellness_entries = {
            entry.date: entry
            for entry in WellnessEntry.objects.filter(
                player=selected_player,
                date__gte=week_start,
                date__lte=latest_session_date,
            )
        }
        rpe_entries = {
            entry.date: entry
            for entry in RPEEntry.objects.filter(
                player=selected_player,
                date__gte=week_start,
                date__lte=latest_session_date,
            )
        }
        mdo_wellness_rows = []
        wellness_scores = []
        rpe_scores = []
        for day in week_dates:
            wellness_entry = wellness_entries.get(day)
            rpe_entry = rpe_entries.get(day)
            wellness_values = []
            if wellness_entry:
                wellness_values = [
                    value for value in (
                        wellness_entry.sleep,
                        wellness_entry.mood,
                        wellness_entry.fitness,
                        wellness_entry.soreness,
                    )
                    if value is not None
                ]
            wellness_avg = round(sum(wellness_values) / len(wellness_values), 1) if wellness_values else None
            if wellness_avg is not None:
                wellness_scores.append(wellness_avg)
            if rpe_entry and rpe_entry.rpe is not None:
                rpe_scores.append(float(rpe_entry.rpe))
            mdo_wellness_rows.append({
                "date": day,
                "label": day.strftime("%d-%m"),
                "wellness_avg": wellness_avg,
                "rpe": rpe_entry.rpe if rpe_entry else None,
                "session_load": rpe_entry.session_load if rpe_entry else None,
                "comment": wellness_entry.comment if wellness_entry else "",
            })

        three_months_ago = today - timedelta(days=90)
        mdo_notes = OverigNote.objects.filter(
            note_type="note",
            page_key="mdo",
            section_key=f"player:{selected_player.id}",
            created_at__date__gte=three_months_ago,
        ).order_by("-created_at", "-id")[:8]
        mdo_action_points = MDOActionPoint.objects.filter(player=selected_player).order_by("is_done", "deadline", "-created_at")[:12]
        mdo_open_action_count = MDOActionPoint.objects.filter(player=selected_player, is_done=False).count()
        mdo_overdue_action_count = MDOActionPoint.objects.filter(
            player=selected_player,
            is_done=False,
            deadline__lt=today,
        ).count()
        mdo_context = {
            "mdo_notes": mdo_notes,
            "mdo_action_points": mdo_action_points,
            "mdo_open_action_count": mdo_open_action_count,
            "mdo_overdue_action_count": mdo_overdue_action_count,
            "mdo_week_rows": mdo_week_rows,
            "mdo_wellness_rows": mdo_wellness_rows,
            "mdo_kpis": {
                "load": round(sum(mdo_load_values), 0),
                "distance_km": round(sum(mdo_td_values) / 1000, 1),
                "sprints": round(sum(mdo_sprints_values), 0),
                "avg_wellness": round(sum(wellness_scores) / len(wellness_scores), 1) if wellness_scores else None,
                "avg_rpe": round(sum(rpe_scores) / len(rpe_scores), 1) if rpe_scores else None,
            },
            "mdo_labels_json": json.dumps(mdo_labels),
            "mdo_td_json": json.dumps(mdo_td_values),
            "mdo_load_json": json.dumps(mdo_load_values),
            "mdo_d15_json": json.dumps(mdo_d15_values),
            "mdo_d20_json": json.dumps(mdo_d20_values),
            "mdo_d25_json": json.dumps(mdo_d25_values),
            "mdo_sprints_json": json.dumps(mdo_sprints_values),
            "mdo_acwr_json": json.dumps(mdo_acwr_values),
        }

        latest_wellness = WellnessEntry.objects.filter(player=selected_player).order_by("-date").first()
        latest_rpe = RPEEntry.objects.filter(player=selected_player).order_by("-date").first()
        latest_speed_test = PlayerSpeedTest.objects.filter(player=selected_player).order_by("-test_date").first()
        latest_team_assignment = (
            selected_player.team_assignments
            .select_related("team")
            .order_by("-start_date")
            .first()
        )
        open_injuries = list(
            InjuryCase.objects
            .select_related("injury_type_ref", "phase_ref", "status_ref")
            .filter(player=selected_player, closed_on__isnull=True)
            .order_by("-started_on", "-created_at")[:3]
        )
        latest_test_rows = fetch_performance_rows("test", selected_player)
        latest_test_rows.sort(key=lambda row: row.get("session_date") or date.min, reverse=True)
        latest_test = latest_test_rows[0] if latest_test_rows else None

        profile_wellness_values = []
        if latest_wellness:
            profile_wellness_values = [
                value for value in (
                    latest_wellness.sleep,
                    latest_wellness.mood,
                    latest_wellness.fitness,
                    latest_wellness.soreness,
                )
                if value is not None
            ]
        profile_wellness_avg = (
            round(sum(profile_wellness_values) / len(profile_wellness_values), 1)
            if profile_wellness_values
            else None
        )
        player_profile_overview = {
            "team": latest_team_assignment.team.name if latest_team_assignment else "",
            "position": selected_player.position_ref.name if selected_player.position_ref else "",
            "latest_wellness": latest_wellness,
            "latest_wellness_avg": profile_wellness_avg,
            "latest_rpe": latest_rpe,
            "latest_gps_date": latest_session_date if current_week_rows else None,
            "week_load": mdo_context["mdo_kpis"]["load"],
            "week_distance_km": mdo_context["mdo_kpis"]["distance_km"],
            "latest_test": latest_test,
            "latest_speed_test": latest_speed_test,
            "open_injuries": open_injuries,
            "open_injury_count": len(open_injuries),
            "latest_program": programma,
            "latest_mdo_note": mdo_notes[0] if mdo_notes else None,
            "open_action_count": mdo_open_action_count,
        }
        mdo_context["player_profile_overview"] = player_profile_overview

    context = {
        "players": players,
        "selected_player": selected_player,
        "selected_team": selected_team_obj,
        "selected_team_code": selected_team_code,
        "selected_team_label": selected_team_label,
        "individual_team_options": academy_context["academy_team_options"],
        "demo_players": academy_context["demo_players"],
        "day_program": day_program,
        "programma": programma,
        "oefeningen": oefeningen,
        "video_previews": video_previews,
        "focus_tab": focus_tab,
        "focus_tab_options": focus_tab_options,
        "focus_tab_label": focus_tab_options.get(focus_tab, "Sprintacceleratie en houding"),
        "active_individual_view": active_view,
        **mdo_context,
    }

    return render(request, "individuele_programmas.html", context)


# -------------------------------------
# PROGRAMMA OPSLAAN (bestaande functie, maar verbeterd)
# -------------------------------------
def individueel_programma_opslaan(request, player_id):
    """
    Slaat een nieuw individueel programma op inclusief oefeningen.
    """
    player = get_object_or_404(Player, id=player_id)

    if request.method == "POST":
        doel = request.POST.get("doel")
        sterke_punten = request.POST.get("sterke_punten", "")
        verbeterpunten = request.POST.get("verbeterpunten", "")
        plan_komende_periode = request.POST.get("plan_komende_periode", "")
        video_links = request.POST.get("video_links", "")
        fysiek_ontwikkelpunt = request.POST.get("fysiek_ontwikkelpunt", "")
        ontwikkelaanpak = request.POST.get("ontwikkelaanpak", "")
        evaluatie_datum = request.POST.get("evaluatie_datum") or None

        programma = Programma.objects.create(
            player=player,
            doel=doel,
            sterke_punten=sterke_punten,
            verbeterpunten=verbeterpunten,
            plan_komende_periode=plan_komende_periode,
            video_links=video_links,
            fysiek_ontwikkelpunt=fysiek_ontwikkelpunt,
            ontwikkelaanpak=ontwikkelaanpak,
            evaluatie_datum=evaluatie_datum,
        )

        exercises = zip(
            request.POST.getlist("exercise_name[]"),
            request.POST.getlist("exercise_duration[]"),
            request.POST.getlist("exercise_rpe[]"),
            request.POST.getlist("exercise_frequency[]"),
            request.POST.getlist("exercise_notes[]"),
        )

        for name, duur, rpe, freq, notes in exercises:
            if name.strip():
                oef = ProgrammaOefening.objects.create(
                    programma=programma,
                    opmerkingen=notes
                )
                oef.naam = name
                oef.duur = duur
                oef.rpe = rpe
                oef.frequentie = freq
                update_fields = []
                if oef.naam_ref_id:
                    update_fields.append("naam_ref")
                if oef.duur_value is not None:
                    update_fields.append("duur_value")
                if oef.duur_unit_ref_id:
                    update_fields.append("duur_unit_ref")
                if oef.duur_text_override:
                    update_fields.append("duur_text_override")
                if oef.rpe_value is not None:
                    update_fields.append("rpe_value")
                if oef.frequentie_ref_id:
                    update_fields.append("frequentie_ref")
                if update_fields:
                    oef.save(update_fields=update_fields)

        messages.success(request, f"Programma voor {player.name} succesvol opgeslagen!")
        return redirect(f"/individuele_programmas/?player_id={player.id}")

    return redirect("individuele_programmas")


def potentials(request):
    players = Player.objects.select_related("position_ref").all().order_by("name")
    selected_player = None

    def potential_notes():
        return OverigNote.objects.filter(
            note_type="potential",
            page_key="potentials",
        ).order_by("-created_at", "-id")

    def potential_player_ids():
        ids = []
        for note in potential_notes():
            raw_id = (note.section_key or "").replace("player:", "", 1)
            if raw_id.isdigit() and int(raw_id) not in ids:
                ids.append(int(raw_id))
        return ids

    def ensure_potential(player, text="High Potential"):
        section_key = f"player:{player.id}"
        note, created = OverigNote.objects.get_or_create(
            note_type="potential",
            page_key="potentials",
            section_key=section_key,
            defaults={"text": text},
        )
        if not created and text and note.text != text:
            note.text = text
            note.save(update_fields=["text"])
        return note

    def get_latest_program(player):
        return Programma.objects.filter(player=player).order_by("-created_at").first()

    def strength_program_key(player):
        return f"strength:{player.id}"

    def empty_strength_program():
        return {
            "thema": "",
            "frequentie": "",
            "doelstelling": "",
            "evaluatie": "",
        }

    def parse_strength_program(note):
        data = empty_strength_program()
        if not note or not note.text:
            return data
        try:
            saved_data = json.loads(note.text)
        except (TypeError, ValueError):
            return data
        for key in data:
            data[key] = saved_data.get(key, "")
        return data

    attention_status_labels = {
        "open": "Open",
        "mee_bezig": "Mee bezig",
        "afgerond": "Afgerond",
    }

    def parse_attention_note(note):
        data = {
            "text": note.text,
            "date": note.created_at.date(),
            "owner": "",
            "status": "open",
            "status_label": attention_status_labels["open"],
            "created_at": timezone.localtime(note.created_at),
        }
        try:
            saved_data = json.loads(note.text)
        except (TypeError, ValueError):
            return data
        if not isinstance(saved_data, dict):
            return data

        raw_date = parse_date(str(saved_data.get("date") or ""))
        status = saved_data.get("status") if saved_data.get("status") in attention_status_labels else "open"
        data.update({
            "text": saved_data.get("text") or "",
            "date": raw_date or note.created_at.date(),
            "owner": saved_data.get("owner") or "",
            "status": status,
            "status_label": attention_status_labels[status],
        })
        return data

    def wants_potential_json():
        return (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            or "application/json" in request.headers.get("accept", "")
        )

    def potential_post_response(url, message, level="success", status=200, payload=None):
        if wants_potential_json():
            data = {
                "ok": level != "error",
                "level": level,
                "message": message,
            }
            if payload:
                data.update(payload)
            return JsonResponse(data, status=status)
        getattr(messages, level)(request, message)
        return redirect(url)

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        selected_player_id = request.POST.get("selected_player_id") or request.POST.get("player_id")

        if action == "add_existing":
            player = get_object_or_404(Player, id=request.POST.get("player_id"))
            ensure_potential(player, request.POST.get("potential_label", "High Potential").strip() or "High Potential")
            messages.success(request, f"Succesvol opgeslagen. {player.name} is toegevoegd aan Potentials.")
            return redirect(f"{reverse('potentials')}?player_id={player.id}")

        if action == "create_player":
            name = (request.POST.get("new_player_name") or "").strip()
            position_name = (request.POST.get("new_player_position") or "").strip()
            if not name:
                messages.error(request, "Vul eerst een spelernaam in.")
                return redirect(reverse("potentials"))
            player = Player.objects.filter(name__iexact=name).first()
            if not player:
                position_obj = None
                if position_name:
                    position_obj, _ = PlayerPosition.objects.get_or_create(name=position_name)
                player = Player.objects.create(name=name, position_ref=position_obj, is_active=True)
                PlayerMonitoringProfile.objects.get_or_create(player=player)
            ensure_potential(player)
            messages.success(request, f"Succesvol opgeslagen. {player.name} is toegevoegd aan Potentials.")
            return redirect(f"{reverse('potentials')}?player_id={player.id}")

        if selected_player_id:
            selected_player = get_object_or_404(Player, id=selected_player_id)
            ensure_potential(selected_player)

        if action == "save_program" and selected_player:
            program_id = request.POST.get("program_id")
            programma = Programma.objects.filter(player=selected_player, id=program_id).first() if program_id else None
            if not programma:
                programma = Programma(player=selected_player)
            programma.doel = (request.POST.get("doel") or "").strip()
            programma.sterke_punten = (request.POST.get("sterke_punten") or "").strip()
            programma.verbeterpunten = (request.POST.get("verbeterpunten") or "").strip()
            programma.plan_komende_periode = (request.POST.get("plan_komende_periode") or "").strip()
            programma.fysiek_ontwikkelpunt = (request.POST.get("fysiek_ontwikkelpunt") or "").strip()
            programma.ontwikkelaanpak = (request.POST.get("ontwikkelaanpak") or "").strip()
            programma.video_links = (request.POST.get("video_links") or "").strip()
            programma.evaluatie_datum = parse_date(request.POST.get("evaluatie_datum") or "")
            programma.save()
            return potential_post_response(
                f"{reverse('potentials')}?player_id={selected_player.id}",
                "Succesvol opgeslagen. Individueel programma bijgewerkt.",
                payload={"program_id": programma.id},
            )

        if action == "save_strength_program" and selected_player:
            strength_data = {
                "thema": (request.POST.get("strength_thema") or "").strip(),
                "frequentie": (request.POST.get("strength_frequentie") or "").strip(),
                "doelstelling": (request.POST.get("strength_doelstelling") or "").strip(),
                "evaluatie": (request.POST.get("strength_evaluatie") or "").strip(),
            }
            note = OverigNote.objects.filter(
                note_type="section",
                page_key="potentials",
                section_key=strength_program_key(selected_player),
            ).first()
            if note:
                note.text = json.dumps(strength_data, ensure_ascii=False)
                note.save(update_fields=["text"])
            else:
                OverigNote.objects.create(
                    note_type="section",
                    page_key="potentials",
                    section_key=strength_program_key(selected_player),
                    text=json.dumps(strength_data, ensure_ascii=False),
                )
            return potential_post_response(
                f"{reverse('potentials')}?player_id={selected_player.id}",
                "Succesvol opgeslagen. Krachtprogramma bijgewerkt.",
            )

        if action == "add_attention" and selected_player:
            text = (request.POST.get("attention_text") or "").strip()
            if text:
                attention_date = parse_date(request.POST.get("attention_date") or "") or timezone.localdate()
                attention_owner = (request.POST.get("attention_owner") or "").strip()
                attention_status = (request.POST.get("attention_status") or "open").strip()
                if attention_status not in attention_status_labels:
                    attention_status = "open"
                note_data = {
                    "text": text,
                    "date": attention_date.isoformat(),
                    "owner": attention_owner,
                    "status": attention_status,
                }
                note = OverigNote.objects.create(
                    note_type="note",
                    page_key="potentials",
                    section_key=f"player:{selected_player.id}",
                    text=json.dumps(note_data, ensure_ascii=False),
                )
                return potential_post_response(
                    f"{reverse('potentials')}?player_id={selected_player.id}",
                    "Succesvol opgeslagen. Aandachtspunt toegevoegd.",
                    payload={
                        "reset_form": True,
                        "item_type": "attention",
                        "item": {
                            "text": text,
                            "date": attention_date.strftime("%d-%m-%Y"),
                            "owner": attention_owner,
                            "status": attention_status,
                            "status_label": attention_status_labels[attention_status],
                            "created_at": timezone.localtime(note.created_at).strftime("%d-%m-%Y %H:%M"),
                        },
                    },
                )
            else:
                return potential_post_response(
                    f"{reverse('potentials')}?player_id={selected_player.id}",
                    "Vul eerst een aandachtspunt in.",
                    level="error",
                    status=400,
                )

        if action == "add_exercise" and selected_player:
            programma = get_latest_program(selected_player) or Programma.objects.create(
                player=selected_player,
                doel="Individueel programma",
            )
            exercise_name = (request.POST.get("exercise_name") or "").strip()
            if not exercise_name:
                return potential_post_response(
                    f"{reverse('potentials')}?player_id={selected_player.id}",
                    "Vul eerst een oefening in.",
                    level="error",
                    status=400,
                )

            naam_ref, _ = ProgrammaOefeningNaam.objects.get_or_create(name=exercise_name)
            frequentie_raw = (request.POST.get("exercise_frequency") or "").strip()
            frequentie_ref = None
            if frequentie_raw:
                frequentie_ref, _ = ProgrammaFrequentie.objects.get_or_create(name=frequentie_raw)
            duur_raw = (request.POST.get("exercise_duration") or "").strip()
            duur_unit_ref = None
            if duur_raw:
                duur_unit_ref, _ = ProgrammaDuurUnit.objects.get_or_create(name="min")
            try:
                rpe_value = int(request.POST.get("exercise_rpe") or 0) or None
            except ValueError:
                rpe_value = None

            oefening = ProgrammaOefening.objects.create(
                programma=programma,
                naam_ref=naam_ref,
                frequentie_ref=frequentie_ref,
                duur_text_override=duur_raw,
                duur_unit_ref=duur_unit_ref,
                rpe_value=rpe_value,
                opmerkingen=(request.POST.get("exercise_notes") or "").strip(),
            )
            return potential_post_response(
                f"{reverse('potentials')}?player_id={selected_player.id}",
                "Succesvol opgeslagen. Oefening toegevoegd.",
                payload={
                    "reset_form": True,
                    "program_id": programma.id,
                    "item_type": "exercise",
                    "item": {
                        "name": oefening.naam_ref.name if oefening.naam_ref else "-",
                        "duration": oefening.duur_text_override or "-",
                        "rpe": oefening.rpe_value or "-",
                        "frequency": oefening.frequentie_ref.name if oefening.frequentie_ref else "-",
                        "notes": oefening.opmerkingen or "-",
                    },
                },
            )

        if action == "remove_potential" and selected_player:
            OverigNote.objects.filter(
                note_type="potential",
                page_key="potentials",
                section_key=f"player:{selected_player.id}",
            ).delete()
            messages.success(request, f"{selected_player.name} is uit Potentials gehaald.")
            return redirect(reverse("potentials"))

    potential_ids = potential_player_ids()
    potential_players = list(
        Player.objects
        .select_related("position_ref")
        .filter(id__in=potential_ids)
        .order_by("name")
    )
    potential_id_set = {player.id for player in potential_players}
    available_players = players.exclude(id__in=potential_id_set)

    selected_player_id = request.GET.get("player_id")
    if selected_player_id:
        selected_player = Player.objects.select_related("position_ref").filter(id=selected_player_id).first()

    programma = get_latest_program(selected_player) if selected_player else None
    oefeningen = []
    attention_notes = []
    latest_wellness = None
    latest_rpe = None
    latest_speed_test = None
    latest_test = None
    potential_percentiles = {}
    week_load = 0
    week_distance = 0
    week_sprints = 0
    recent_tests = []
    gps_week_rows = []
    gps_labels_json = "[]"
    gps_td_json = "[]"
    gps_load_json = "[]"
    gps_d15_json = "[]"
    gps_sprints_json = "[]"
    gps_acwr_json = "[]"
    attendance_rows = []
    attendance_total_count = 0
    attendance_present_count = 0
    attendance_percentage = None
    latest_weight = None
    weight_rows = []
    latest_anthropometry = None
    anthropometry_rows = []
    weight_chart_labels_json = "[]"
    weight_chart_values_json = "[]"
    length_chart_labels_json = "[]"
    length_chart_values_json = "[]"
    latest_beweeganalyse_sessie = None
    beweeganalyse_scores = []
    beweeganalyse_attention_points = []
    beweeganalyse_average_score = None
    strength_program = empty_strength_program()

    if selected_player:
        if programma:
            oefeningen = ProgrammaOefening.objects.select_related(
                "naam_ref",
                "frequentie_ref",
                "duur_unit_ref",
            ).filter(programma=programma).order_by("id")
        attention_notes = [
            parse_attention_note(note)
            for note in OverigNote.objects.filter(
                note_type="note",
                page_key="potentials",
                section_key=f"player:{selected_player.id}",
            ).order_by("-created_at", "-id")[:8]
        ]
        strength_note = OverigNote.objects.filter(
            note_type="section",
            page_key="potentials",
            section_key=strength_program_key(selected_player),
        ).first()
        strength_program = parse_strength_program(strength_note)
        latest_wellness = WellnessEntry.objects.filter(player=selected_player).order_by("-date").first()
        latest_rpe = RPEEntry.objects.filter(player=selected_player).order_by("-date").first()
        latest_speed_test = PlayerSpeedTest.objects.filter(player=selected_player).order_by("-test_date").first()
        latest_session_date = timezone.localdate()
        all_test_rows = fetch_performance_rows("test")
        test_rows = sorted(
            [row for row in all_test_rows if row["player_id"] == selected_player.id],
            key=lambda row: row.get("session_date") or date.min,
            reverse=True,
        )
        recent_tests = test_rows[:8]
        latest_test = recent_tests[0] if recent_tests else None

        def metric_values(code):
            values = []
            for row in all_test_rows:
                raw_value = row.get(code)
                if raw_value is not None:
                    try:
                        values.append(float(raw_value))
                    except (TypeError, ValueError):
                        pass
            return values

        def percentile(value, code, reverse=False):
            values = metric_values(code)
            if value is None or not values:
                return None
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                return None
            min_value = min(values)
            max_value = max(values)
            if min_value == max_value:
                return 50
            if reverse:
                return round(100 * (max_value - numeric) / (max_value - min_value))
            return round(100 * (numeric - min_value) / (max_value - min_value))

        if latest_test:
            potential_percentiles = {
                "sprint": percentile(latest_test.get("sprint_10"), "sprint_10", reverse=True),
                "cmj": percentile(latest_test.get("cmj"), "cmj"),
                "isrt": percentile(latest_test.get("isrt"), "isrt"),
                "submax": percentile(latest_test.get("submax"), "submax"),
            }
        performance_rows = [
            *fetch_performance_rows("training", selected_player),
            *fetch_performance_rows("match", selected_player),
        ]
        if performance_rows:
            latest_session_date = max(
                (row.get("session_date") for row in performance_rows if row.get("session_date")),
                default=latest_session_date,
            )
        week_start = latest_session_date - timedelta(days=6)
        week_rows = [
            row for row in performance_rows
            if row.get("session_date") and week_start <= row["session_date"] <= latest_session_date
        ]

        def row_float(row, key):
            try:
                return float(row.get(key) or 0)
            except (TypeError, ValueError):
                return 0.0

        week_load = round(sum(row_float(row, "load") for row in week_rows), 0)
        week_distance = round(sum(row_float(row, "total_distance") for row in week_rows) / 1000, 1)
        week_sprints = round(sum(row_float(row, "sprints") for row in week_rows), 0)
        day_names_short = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
        gps_week_rows = []
        gps_labels = []
        gps_td_values = []
        gps_load_values = []
        gps_d15_values = []
        gps_sprints_values = []
        gps_acwr_values = []
        previous_start = week_start - timedelta(days=21)
        previous_rows = [
            row for row in performance_rows
            if row.get("session_date") and previous_start <= row["session_date"] < week_start
        ]
        chronic_daily_load = sum(row_float(row, "load") for row in previous_rows) / 21 if previous_rows else 0
        for day_offset in range(7):
            current_day = week_start + timedelta(days=day_offset)
            day_rows = [row for row in week_rows if row.get("session_date") == current_day]
            day_label = f"{day_names_short[current_day.weekday()]} {current_day.strftime('%d-%m')}"
            load = round(sum(row_float(row, "load") for row in day_rows), 0)
            distance_m = round(sum(row_float(row, "total_distance") for row in day_rows), 1)
            distance_km = round(distance_m / 1000, 2)
            sprints = round(sum(row_float(row, "sprints") for row in day_rows), 0)
            hsd = round(sum(row_float(row, "hsd") for row in day_rows), 0)
            acwr = round(load / chronic_daily_load, 2) if chronic_daily_load else 0
            gps_labels.append(day_label)
            gps_td_values.append(distance_m)
            gps_load_values.append(load)
            gps_d15_values.append(hsd)
            gps_sprints_values.append(sprints)
            gps_acwr_values.append(acwr)
            gps_week_rows.append({
                "label": day_label,
                "load": load,
                "distance_km": distance_km,
                "sprints": sprints,
                "hsd": hsd,
            })
        gps_labels_json = json.dumps(gps_labels)
        gps_td_json = json.dumps(gps_td_values)
        gps_load_json = json.dumps(gps_load_values)
        gps_d15_json = json.dumps(gps_d15_values)
        gps_sprints_json = json.dumps(gps_sprints_values)
        gps_acwr_json = json.dumps(gps_acwr_values)
        attendance_qs = (
            AttendanceRecord.objects
            .select_related("status")
            .filter(player=selected_player, date__gte=timezone.localdate() - timedelta(days=30))
            .order_by("-date")
        )
        attendance_total_count = attendance_qs.count()
        attendance_present_count = attendance_qs.filter(completed=True).count()
        attendance_percentage = round((attendance_present_count / attendance_total_count) * 100) if attendance_total_count else None
        attendance_rows = attendance_qs[:10]
        weight_rows = list(WeightEntry.objects.filter(player=selected_player).order_by("-date")[:8])
        latest_weight = weight_rows[0] if weight_rows else None
        anthropometry_rows = list(AnthropometrySession.objects.filter(player=selected_player).order_by("-date", "-id")[:5])
        latest_anthropometry = anthropometry_rows[0] if anthropometry_rows else None
        weight_history = list(WeightEntry.objects.filter(player=selected_player).order_by("date", "id"))
        length_history = [
            row for row in AnthropometrySession.objects.filter(
                player=selected_player,
                length__isnull=False,
            ).order_by("date", "id")
        ]
        weight_chart_labels_json = json.dumps([row.date.strftime("%d-%m-%Y") for row in weight_history])
        weight_chart_values_json = json.dumps([round(float(row.weight), 1) for row in weight_history])
        length_chart_labels_json = json.dumps([row.date.strftime("%d-%m-%Y") for row in length_history])
        length_chart_values_json = json.dumps([round(float(row.length), 1) for row in length_history])
        latest_beweeganalyse_sessie = (
            BeweeganalyseSessie.objects
            .filter(player=selected_player)
            .prefetch_related("beoordelingen__punt__onderdeel")
            .order_by("-date", "-updated_at", "-id")
            .first()
        )
        if latest_beweeganalyse_sessie:
            beweeganalyse_scores = sorted(
                latest_beweeganalyse_sessie.beoordelingen.all(),
                key=lambda beoordeling: (
                    beoordeling.punt.onderdeel.sort_order,
                    beoordeling.punt.sort_order,
                    beoordeling.punt.title,
                ),
            )
            scored_values = [score.score for score in beweeganalyse_scores if score.score is not None]
            beweeganalyse_average_score = round(sum(scored_values) / len(scored_values), 1) if scored_values else None
            beweeganalyse_attention_points = [
                score for score in beweeganalyse_scores
                if score.priority_flag or (score.comment or "").strip()
            ]

    return render(request, "potentials.html", {
        "players": players,
        "available_players": available_players,
        "potential_players": potential_players,
        "selected_player": selected_player,
        "programma": programma,
        "oefeningen": oefeningen,
        "attention_notes": attention_notes,
        "latest_wellness": latest_wellness,
        "latest_rpe": latest_rpe,
        "latest_speed_test": latest_speed_test,
        "latest_test": latest_test,
        "potential_percentiles": potential_percentiles,
        "week_load": week_load,
        "week_distance": week_distance,
        "week_sprints": week_sprints,
        "recent_tests": recent_tests,
        "gps_week_rows": gps_week_rows,
        "gps_labels_json": gps_labels_json,
        "gps_td_json": gps_td_json,
        "gps_load_json": gps_load_json,
        "gps_d15_json": gps_d15_json,
        "gps_sprints_json": gps_sprints_json,
        "gps_acwr_json": gps_acwr_json,
        "attendance_rows": attendance_rows,
        "attendance_total_count": attendance_total_count,
        "attendance_present_count": attendance_present_count,
        "attendance_percentage": attendance_percentage,
        "latest_weight": latest_weight,
        "weight_rows": weight_rows,
        "latest_anthropometry": latest_anthropometry,
        "anthropometry_rows": anthropometry_rows,
        "weight_chart_labels_json": weight_chart_labels_json,
        "weight_chart_values_json": weight_chart_values_json,
        "length_chart_labels_json": length_chart_labels_json,
        "length_chart_values_json": length_chart_values_json,
        "latest_beweeganalyse_sessie": latest_beweeganalyse_sessie,
        "beweeganalyse_scores": beweeganalyse_scores,
        "beweeganalyse_attention_points": beweeganalyse_attention_points,
        "beweeganalyse_average_score": beweeganalyse_average_score,
        "strength_program": strength_program,
    })

def rpe_view(request):
    """Oude RPE-ingang doorsturen naar het gecombineerde Wellness & RPE overzicht."""
    if request.method == "POST":
        return rpe_view_old(request)
    return redirect("/wellness/")


def _wellness_label(value, labels):
    if value is None:
        return "-"
    return labels.get(value, str(value))


def _wellness_score(entry):
    if not entry:
        return None
    values = [entry.sleep, entry.mood, entry.fitness, entry.soreness]
    values = [value for value in values if value is not None]
    if not values:
        return None
    return round(sum(values) / len(values), 1)


def _wellness_label_sets():
    return {
        "sleep": {1: "Heel goed", 2: "Goed", 3: "Oké", 4: "Slecht"},
        "mood": {1: "Heel goed", 2: "Goed", 3: "Matig", 4: "Slecht"},
        "fitness": {1: "Heel fit", 2: "Fit", 3: "Oké", 4: "Vermoeid"},
        "soreness": {1: "Geen", 2: "Licht", 3: "Veel"},
    }


def _clean_int_or_none(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def rpe_view_old(request):
    """RPE dashboard met robuuste POST-afhandeling en 3NF velden."""

    player_app_user = _is_player_app_user(request.user)
    player_app_player = _player_for_user(request.user) if player_app_user else None
    players_qs = Player.objects.select_related("monitoring_profile").all().order_by("name")
    if player_app_user:
        players_qs = players_qs.filter(id=player_app_player.id) if player_app_player else players_qs.none()
    players = list(players_qs)
    training_types = RPETrainingType.objects.filter(is_active=True).order_by("name")
    today = timezone.now().date()

    def _parse_rpe_date(raw_value):
        raw_value = (raw_value or "").strip()
        if not raw_value:
            return today

        parsed = parse_date(raw_value)  # yyyy-mm-dd
        if parsed:
            return parsed

        # Fallbacks: dd-mm-yyyy of dd/mm/yyyy
        for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(raw_value, fmt).date()
            except ValueError:
                continue
        return None

    if request.method == "POST":
        player_id_raw = (request.POST.get("player_id") or "").strip()
        rpe_raw = (request.POST.get("rpe") or "").strip()
        training_type_raw = (request.POST.get("training_type") or "").strip()
        date_raw = request.POST.get("date")

        errors = []

        if player_app_user and (not player_app_player or str(player_app_player.id) != player_id_raw):
            raise PermissionDenied

        player = Player.objects.filter(id=player_id_raw).first()
        if not player:
            errors.append("Ongeldige speler.")

        date_value = _parse_rpe_date(date_raw)
        if not date_value:
            errors.append("Ongeldige datum. Gebruik dd-mm-jjjj of jjjj-mm-dd.")

        try:
            rpe_value = int(rpe_raw)
            if rpe_value < 1 or rpe_value > 10:
                raise ValueError
        except (TypeError, ValueError):
            rpe_value = None
            errors.append("RPE moet een getal tussen 1 en 10 zijn.")

        training_type_obj = None
        if training_type_raw:
            if training_type_raw.isdigit():
                training_type_obj = RPETrainingType.objects.filter(id=int(training_type_raw)).first()
            else:
                training_type_obj = RPETrainingType.objects.filter(name__iexact=training_type_raw).first()
            if not training_type_obj:
                errors.append("Ongeldig trainingstype.")

        if errors:
            for err in errors:
                messages.error(request, err)
            return redirect("/rpe/")

        try:
            _, created = RPEEntry.objects.update_or_create(
                player=player,
                date=date_value,
                defaults={
                    "rpe": rpe_value,
                    "training_type_ref": training_type_obj,
                },
            )
            if created:
                messages.success(request, f"RPE opgeslagen voor {player.name}.")
            else:
                messages.success(request, f"RPE bijgewerkt voor {player.name}.")
        except Exception:
            messages.error(request, "Opslaan van RPE is mislukt. Controleer invoer of databaseverbinding.")

        return redirect("/rpe/")

    todays_rpe = RPEEntry.objects.select_related("player", "training_type_ref").filter(date=today)
    players_with_rpe = {entry.player_id for entry in todays_rpe}
    not_filled = [p for p in players if p.id not in players_with_rpe]
    filled = todays_rpe.order_by("player__name")

    context = {
        "players": players,
        "training_types": training_types,
        "today": today,
        "not_filled": not_filled,
        "filled": filled,
    }

    return render(request, "rpe.html", context)

def wellness(request):
    """Wellness dashboard met onderscheid tussen ingevuld en niet ingevuld."""
    player_app_user = _is_player_app_user(request.user)
    player_app_player = _player_for_user(request.user) if player_app_user else None

    # 1ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ Datum ophalen & converteren naar date-object
    selected_date = request.GET.get("date")

    if selected_date:
        # GET levert een string -> converteren naar date
        date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        date = timezone.now().date()

    wellness_team_codes = _attendance_team_codes()
    selected_team_code = (request.GET.get("team") or wellness_team_codes[0]).strip().upper()
    if selected_team_code not in wellness_team_codes:
        selected_team_code = wellness_team_codes[0]
    selected_team, team_players_qs = _team_players_for_gps_upload(selected_team_code)
    selected_team_label = selected_team.name if selected_team else _academy_team_label(selected_team_code)

    # 2ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ Spelers ophalen
    players_qs = Player.objects.select_related("monitoring_profile").all().order_by("name")
    if player_app_user:
        players_qs = players_qs.filter(id=player_app_player.id) if player_app_player else players_qs.none()
    else:
        team_player_ids = set(team_players_qs.values_list("id", flat=True))
        players_qs = players_qs.filter(id__in=team_player_ids) if team_player_ids else players_qs.none()
    players = list(players_qs)

    # 3) Entries van deze datum ophalen
    existing_entries = WellnessEntry.objects.select_related("player").filter(date=date, player__in=players)
    rpe_entries = RPEEntry.objects.select_related("player", "training_type_ref").filter(date=date, player__in=players)

    filled_player_ids = set(existing_entries.values_list("player_id", flat=True))
    rpe_by_player = {entry.player_id: entry for entry in rpe_entries}
    for player in players:
        player.today_rpe = rpe_by_player.get(player.id)

    # 4) Verdeling in ingevuld / niet ingevuld
    players_filled = [p for p in players if p.id in filled_player_ids]
    players_not_filled = [p for p in players if p.id not in filled_player_ids]

    # 5ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ POST: wellness opslaan
    if request.method == "POST":
        player_id = request.POST.get("player_id")
        sleep = request.POST.get("sleep")
        mood = request.POST.get("mood")
        fitness = request.POST.get("fitness")
        soreness = request.POST.get("soreness")
        comment = request.POST.get("comment")
        srpe = _clean_int_or_none(request.POST.get("srpe"))
        date_post = request.POST.get("date")

        # Datum van POST opnieuw correct converteren
        date_obj = datetime.strptime(date_post, "%Y-%m-%d").date()

        player = get_object_or_404(Player, id=player_id)
        if player_app_user and (not player_app_player or player.id != player_app_player.id):
            raise PermissionDenied

        WellnessEntry.objects.update_or_create(
            player=player,
            date=date_obj,
            defaults={
                "sleep": _clean_int_or_none(sleep),
                "mood": _clean_int_or_none(mood),
                "fitness": _clean_int_or_none(fitness),
                "soreness": _clean_int_or_none(soreness),
                "comment": comment
            }
        )

        if srpe is not None:
            RPEEntry.objects.update_or_create(
                player=player,
                date=date_obj,
                defaults={"rpe": srpe},
            )

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "ok": True,
                    "message": "Succesvol opgeslagen.",
                    "player_id": player.id,
                    "player_name": player.name,
                    "date": date_obj.isoformat(),
                    "has_wellness": True,
                    "has_rpe": srpe is not None,
                }
            )

        # Refresh pagina zodat speler naar 'wel ingevuld' gaat
        redirect_url = f"/wellness/?date={date_obj}"
        if not player_app_user:
            redirect_url = f"{redirect_url}&team={selected_team_code}"
        return redirect(redirect_url)

    wellness_by_player = {entry.player_id: entry for entry in existing_entries}
    wellness_rows = []
    for entry in existing_entries.order_by("player__name"):
        entry.rpe_entry = rpe_by_player.get(entry.player_id)
        wellness_rows.append(entry)
    wellness_labels = _wellness_label_sets()
    combined_rows = []
    for player in players:
        wellness_entry = wellness_by_player.get(player.id)
        rpe_entry = rpe_by_player.get(player.id)
        if not wellness_entry and not rpe_entry:
            continue
        combined_rows.append({
            "player": player,
            "wellness": wellness_entry,
            "rpe": rpe_entry,
            "wellness_score": _wellness_score(wellness_entry),
            "sleep_label": _wellness_label(wellness_entry.sleep if wellness_entry else None, wellness_labels["sleep"]),
            "mood_label": _wellness_label(wellness_entry.mood if wellness_entry else None, wellness_labels["mood"]),
            "fitness_label": _wellness_label(wellness_entry.fitness if wellness_entry else None, wellness_labels["fitness"]),
            "soreness_label": _wellness_label(wellness_entry.soreness if wellness_entry else None, wellness_labels["soreness"]),
        })
    previous_day = date - timedelta(days=1)
    next_day = date + timedelta(days=1)
    total_players = len(players)
    wellness_count = len(players_filled)
    rpe_count = len(rpe_by_player)
    wellness_percentage = round((wellness_count / total_players) * 100) if total_players else None
    rpe_percentage = round((rpe_count / total_players) * 100) if total_players else None

    # 6) Context + render
    return render(request, "wellness.html", {
        "date": date.strftime("%Y-%m-%d"),
        "date_obj": date,
        "previous_day": previous_day,
        "next_day": next_day,
        "player_app_user": player_app_user,
        "player_app_player": player_app_player,
        "wellness_team_options": _attendance_team_options(),
        "selected_team_code": selected_team_code,
        "selected_team_label": selected_team_label,
        "total_players": total_players,
        "wellness_count": wellness_count,
        "rpe_count": rpe_count,
        "wellness_percentage": wellness_percentage,
        "rpe_percentage": rpe_percentage,
        "players_filled": players_filled,
        "players_not_filled": players_not_filled,
        "existing_entries": existing_entries,
        "wellness_rows": wellness_rows,
        "rpe_entries": rpe_entries,
        "rpe_by_player": rpe_by_player,
        "combined_rows": combined_rows,
    })



# =====================================
#   HIT PAGINA VIEW
# =====================================

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Player, PlayerSpeedTest, HitAsrPlanSession, HitAsrPlanEntry


def hit_page(request):
    """HIT pagina: calculator + individualiserings-tools."""
    hit_redirect_url = request.path
    action = request.POST.get("asr_form_action") if request.method == "POST" else None

    if request.method == "POST" and action == "save_asr_tests":
        test_date_raw = (request.POST.get("asr_test_date") or "").strip()
        try:
            test_date = datetime.strptime(test_date_raw, "%Y-%m-%d").date() if test_date_raw else datetime.today().date()
        except ValueError:
            test_date = datetime.today().date()

        player_ids = request.POST.getlist("asr_player_id[]")
        mss_values = request.POST.getlist("asr_mss[]")
        mas_values = request.POST.getlist("asr_mas[]")

        saved = 0
        for i, player_id in enumerate(player_ids):
            player_id = (player_id or "").strip()
            if not player_id:
                continue
            mss_raw = (mss_values[i] if i < len(mss_values) else "").strip()
            mas_raw = (mas_values[i] if i < len(mas_values) else "").strip()
            if not mss_raw or not mas_raw:
                continue
            try:
                player = Player.objects.get(id=player_id)
                mss = float(mss_raw.replace(",", "."))
                mas = float(mas_raw.replace(",", "."))
            except (Player.DoesNotExist, ValueError):
                continue
            if mss <= 0 or mas <= 0:
                continue
            PlayerSpeedTest.objects.update_or_create(
                player=player,
                test_date=test_date,
                defaults={"mss_kmh": mss, "mas_kmh": mas},
            )
            saved += 1

        if saved:
            messages.success(request, f"{saved} MSS/MAS testwaarden opgeslagen voor {test_date}.")
        else:
            messages.warning(request, "Geen geldige MSS/MAS testwaarden opgeslagen.")
        return redirect(hit_redirect_url)

    if request.method == "POST" and action == "save_asr_plan":
        plan_date_raw = (request.POST.get("asr_plan_date") or "").strip()
        try:
            plan_date = datetime.strptime(plan_date_raw, "%Y-%m-%d").date() if plan_date_raw else datetime.today().date()
        except ValueError:
            plan_date = datetime.today().date()

        try:
            mas_percent = float((request.POST.get("asr_mas_percent") or "0").replace(",", "."))
        except ValueError:
            mas_percent = 0.0
        try:
            reference_speed = float((request.POST.get("asr_reference_speed_kmh") or "0").replace(",", "."))
        except ValueError:
            reference_speed = 0.0

        if mas_percent <= 0:
            messages.warning(request, "Ongeldige intensiteit (%MAS).")
            return redirect(hit_redirect_url)

        player_ids = request.POST.getlist("asr_player_id[]")
        mss_values = request.POST.getlist("asr_mss[]")
        mas_values = request.POST.getlist("asr_mas[]")

        rows = []
        for i, player_id in enumerate(player_ids):
            player_id = (player_id or "").strip()
            if not player_id:
                continue
            try:
                mss = float((mss_values[i] if i < len(mss_values) else "").replace(",", "."))
                mas = float((mas_values[i] if i < len(mas_values) else "").replace(",", "."))
            except ValueError:
                continue
            if mss <= 0 or mas <= 0:
                continue
            try:
                player = Player.objects.get(id=player_id)
            except Player.DoesNotExist:
                continue

            target_speed = mas * (mas_percent / 100.0)
            asr = mss - mas
            pct_asr = None
            indication = None
            if asr <= 0:
                indication = "MSS <= MAS"
            else:
                pct_asr = ((target_speed - mas) / asr) * 100.0
                if pct_asr < 0:
                    indication = "Onder MAS"
                elif pct_asr < 30:
                    indication = "Laag"
                elif pct_asr < 60:
                    indication = "Midden"
                elif pct_asr < 80:
                    indication = "Hoog"
                elif pct_asr <= 100:
                    indication = "Zeer hoog"
                else:
                    indication = "Boven MSS"

            rows.append(
                {
                    "player": player,
                    "mss_kmh": round(mss, 2),
                    "mas_kmh": round(mas, 2),
                    "target_speed_kmh": round(target_speed, 2),
                    "asr_kmh": round(asr, 2),
                    "pct_mas": round(mas_percent, 2),
                    "pct_asr": round(pct_asr, 2) if pct_asr is not None else None,
                    "indication": indication,
                }
            )

        if not rows:
            messages.warning(request, "Geen geldige spelersregels om ASR-planning op te slaan.")
            return redirect(hit_redirect_url)

        with transaction.atomic():
            plan = HitAsrPlanSession.objects.create(
                session_date=plan_date,
                mas_percent=round(mas_percent, 2),
                reference_speed_kmh=round(reference_speed, 2) if reference_speed > 0 else None,
            )
            HitAsrPlanEntry.objects.bulk_create(
                [
                    HitAsrPlanEntry(session=plan, **row)
                    for row in rows
                ]
            )
        messages.success(request, f"ASR-planning opgeslagen ({len(rows)} spelers) voor {plan_date}.")
        return redirect(hit_redirect_url)

    players = Player.objects.select_related("monitoring_profile").all().order_by("name")
    latest_by_player = {}
    latest_tests = PlayerSpeedTest.objects.select_related("player").order_by("player_id", "-test_date", "-updated_at", "-id")
    for test in latest_tests:
        if test.player_id in latest_by_player:
            continue
        latest_by_player[test.player_id] = {
            "mss": float(test.mss_kmh),
            "mas": float(test.mas_kmh),
            "test_date": test.test_date.isoformat(),
        }

    recent_asr_plans = (
        HitAsrPlanSession.objects.prefetch_related("entries__player")
        .all()[:5]
    )

    context = {
        "players": players,
        "asr_latest_map": latest_by_player,
        "asr_test_date": datetime.today().date().isoformat(),
        "asr_plan_date": datetime.today().date().isoformat(),
        "recent_asr_plans": recent_asr_plans,
    }
    return render(request, "hit.html", context)




# -------------------------------------
# AANWEZIGHEDEN PAGINA
# -------------------------------------
def aanwezigheden_pagina(request):
    """Overzicht van aanwezigheden per dag (ACADATA-stijl)."""

    # 1. Datum ophalen of vandaag gebruiken
    date_str = request.GET.get("date")
    if date_str:
        chosen_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        chosen_date = datetime.today().date()

    # 2. Team en spelers ophalen
    attendance_team_codes = _attendance_team_codes()
    selected_team_code = (request.GET.get("team") or attendance_team_codes[0]).strip().upper()
    if selected_team_code not in attendance_team_codes:
        selected_team_code = attendance_team_codes[0]
    selected_team, team_players_qs = _team_players_for_gps_upload(selected_team_code)
    selected_team_label = selected_team.name if selected_team else _academy_team_label(selected_team_code)
    players = list(team_players_qs.select_related("monitoring_profile", "position_ref"))

    agenda_status, agenda_entry = _attendance_status_from_agenda(chosen_date, selected_team_code)

    status_qs = AttendanceStatus.objects.filter(is_active=True).order_by("sort_order", "label")
    status_choices = [(status.code, status.label) for status in status_qs]
    fallback_status = status_qs.filter(code="overig").first() or status_qs.first()
    default_status = agenda_status or fallback_status

    # 3. AttendanceRecords in bulk ophalen/aanmaken, zodat grote teams niet per speler losse queries doen.
    player_ids = [player.id for player in players]
    attendance_qs = (
        AttendanceRecord.objects
        .select_related("player", "player__position_ref", "status")
        .filter(player_id__in=player_ids, date=chosen_date)
    )
    attendance_by_player = {record.player_id: record for record in attendance_qs}
    missing_records = [
        AttendanceRecord(player=player, date=chosen_date, status=default_status, completed=False)
        for player in players
        if player.id not in attendance_by_player and default_status
    ]
    if missing_records:
        AttendanceRecord.objects.bulk_create(missing_records, ignore_conflicts=True)
        attendance_by_player = {
            record.player_id: record
            for record in (
                AttendanceRecord.objects
                .select_related("player", "player__position_ref", "status")
                .filter(player_id__in=player_ids, date=chosen_date)
            )
        }

    if agenda_status:
        agenda_update_ids = [
            record.id
            for record in attendance_by_player.values()
            if (
                not record.completed
                and record.status
                and record.status.code == "overig"
                and record.status_id != agenda_status.id
            )
        ]
        if agenda_update_ids:
            AttendanceRecord.objects.filter(id__in=agenda_update_ids).update(
                status=agenda_status,
                updated_at=timezone.now(),
            )
            attendance_by_player = {
                record.player_id: record
                for record in (
                    AttendanceRecord.objects
                    .select_related("player", "player__position_ref", "status")
                    .filter(player_id__in=player_ids, date=chosen_date)
                )
            }

    records = []
    for player in players:
        aanwezigheid = attendance_by_player.get(player.id)
        if not aanwezigheid:
            continue
        records.append(
            SimpleNamespace(
                id=aanwezigheid.id,
                player=player,
                status=aanwezigheid.status.code if aanwezigheid.status else "overig",
                status_label=aanwezigheid.status.label if aanwezigheid.status else "Overig",
                completed=aanwezigheid.completed,
                date=aanwezigheid.date,
                team_code=selected_team_code,
                position=player.position_ref.name if player.position_ref else "",
            )
        )

    # 4. Navigatie (vorige dag / volgende dag)
    previous_day = chosen_date - timedelta(days=1)
    next_day = chosen_date + timedelta(days=1)
    completed_count = sum(1 for record in records if record.completed)
    registered_count = len(records)
    attendance_percentage = round((completed_count / registered_count) * 100) if registered_count else None

    context = {
        "players": players,
        "records": records,
        "chosen_date": chosen_date,
        "previous_day": previous_day,
        "next_day": next_day,
        "status_choices": status_choices,
        "attendance_team_options": _attendance_team_options(),
        "selected_team_code": selected_team_code,
        "selected_team_label": selected_team_label,
        "agenda_suggestion": agenda_entry,
        "completed_count": completed_count,
        "registered_count": registered_count,
        "attendance_percentage": attendance_percentage,
    }

    return render(request, "aanwezigheden.html", context)


# -------------------------------------
# AANWEZIGHEDEN UPDATE
# -------------------------------------
def aanwezigheden_update(request, record_id):
    """Update ÃƒÆ’Ã‚Â©ÃƒÆ’Ã‚Â©n aanwezigheidsrecord (dropdown + checkmark)."""

    aanwezigheid = get_object_or_404(AttendanceRecord, id=record_id)
    selected_team_code = (request.POST.get("team") or request.GET.get("team") or "").strip().upper()

    if request.method == "POST":
        new_status_code = request.POST.get("status")
        completed = request.POST.get("completed") == "on"
        status = AttendanceStatus.objects.filter(code=new_status_code, is_active=True).first()
        if status is None:
            status = AttendanceStatus.objects.filter(code="overig").first()
        aanwezigheid.status = status
        aanwezigheid.completed = completed
        aanwezigheid.save(update_fields=["status", "completed", "updated_at"])

        messages.success(
            request,
            f"Aanwezigheid bijgewerkt voor {aanwezigheid.player.name}"
        )
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "ok": True,
                    "message": "Succesvol opgeslagen.",
                    "status": aanwezigheid.status.code if aanwezigheid.status else "overig",
                    "status_label": aanwezigheid.status.label if aanwezigheid.status else "Overig",
                    "completed": aanwezigheid.completed,
                }
            )

    redirect_url = f"/aanwezigheden/?date={aanwezigheid.date}"
    if selected_team_code:
        redirect_url = f"{redirect_url}&team={selected_team_code}"
    return redirect(redirect_url)


def overig(request):
    page = request.GET.get('page', 'menu')

    staff_members = Staff.objects.all().order_by('name')
    players = Player.objects.all().order_by('name')

    if page == "hit":
        return redirect("overig_hit")

    def section_text(page_key: str, section_key: str) -> str:
        item = (
            OverigNote.objects
            .filter(note_type="section", page_key=page_key, section_key=section_key)
            .order_by("-created_at")
            .first()
        )
        return (item.text or "") if item else ""

    # ======================================
    # NOTITIES
    # ======================================
    if page == "notities":
        if request.method == 'POST':
            text = request.POST.get('text')
            if text:
                OverigNote.objects.create(
                    note_type="note",
                    page_key="notities",
                    text=text.strip(),
                )
            return redirect('/overig/?page=notities')

        items = OverigNote.objects.filter(note_type="note").order_by('-created_at')
        return render(request, 'overig.html', {
            'page': 'notities',
            'items': items,
            'players': players,
            'staff': staff_members,
        })

    # ======================================
    # POP GESPREKKEN
    # ======================================
    if page == "pop":
        if request.method == "POST":
            for section in ("situatie", "doelen", "reflectie", "actieplan"):
                text = request.POST.get(section, "")
                OverigNote.objects.create(
                    note_type="section",
                    page_key="pop",
                    section_key=section,
                    text=text.strip(),
                )
            return redirect("/overig/?page=pop")

        return render(request, 'overig.html', {
            'page': 'pop',
            'players': players,
            'staff': staff_members,
            "pop_texts": {
                "situatie": section_text("pop", "situatie"),
                "doelen": section_text("pop", "doelen"),
                "reflectie": section_text("pop", "reflectie"),
                "actieplan": section_text("pop", "actieplan"),
            },
        })

    # ======================================
    # HIGH POTENTIALS
    # ======================================
    if page == "hp":
        if request.method == "POST":
            section = request.POST.get("section")
            text = request.POST.get("text", "")
            if section:
                OverigNote.objects.create(
                    note_type="section",
                    page_key="hp",
                    section_key=section,
                    text=text.strip(),
                )
            return redirect("/overig/?page=hp")

        return render(request, 'overig.html', {
            'page': 'hp',
            'players': players,
            'staff': staff_members,
            "hp_texts": {
                "focus": section_text("hp", "focus"),
                "kaders": section_text("hp", "kaders"),
                "monitoring": section_text("hp", "monitoring"),
            },
        })

    # ======================================
    # SPELERSFOTO'S UPLOADEN
    # ======================================
    if page == "jeugd":
        return redirect("/overig/?page=fotos")

    if page == "fotos":
        if request.method == "POST":
            player_id = request.POST.get("player_id")
            image = request.FILES.get("player_image")

            if not player_id:
                messages.error(request, "Kies eerst een speler.")
                return redirect("/overig/?page=fotos")
            if not image:
                messages.error(request, "Kies een foto om te uploaden.")
                return redirect("/overig/?page=fotos")

            player = get_object_or_404(Player, id=player_id)
            player.image = image
            player.save(update_fields=["image"])
            messages.success(request, f"Succesvol opgeslagen. Foto van {player.name} bijgewerkt.")
            return redirect("/overig/?page=fotos")

        return render(request, 'overig.html', {
            'page': 'fotos',
            'players': players,
            'staff': staff_members,
        })

    # ======================================
    # GENERIEKE OVERIG-SECTIES
    # ======================================
    if page == "staf-aanwezigheden":
        if request.method == "POST":
            section = request.POST.get("section")
            text = request.POST.get("text", "")
            if section:
                OverigNote.objects.create(
                    note_type="section",
                    page_key=page,
                    section_key=section,
                    text=text.strip(),
                )
            return redirect(f"/overig/?page={page}")

        return render(request, 'overig.html', {
            'page': page,
            'players': players,
            'staff': staff_members,
            'staff_presence_texts': {
                'bezetting': section_text(page, 'bezetting'),
                'afwezig': section_text(page, 'afwezig'),
                'locatie': section_text(page, 'locatie'),
                'opvolging': section_text(page, 'opvolging'),
            },
        })

    if page == "fysiek-wetenschap":
        return redirect("/overig/")

    if page in {"ontwikkelingsgesprekken", "vakantieprogramma"}:
        if request.method == "POST":
            section = request.POST.get("section")
            text = request.POST.get("text", "")
            if section:
                OverigNote.objects.create(
                    note_type="section",
                    page_key=page,
                    section_key=section,
                    text=text.strip(),
                )
            return redirect(f"/overig/?page={page}")

        return render(request, 'overig.html', {
            'page': page,
            'players': players,
            'staff': staff_members,
            'generic_texts': {
                'kader': section_text(page, 'kader'),
                'actueel': section_text(page, 'actueel'),
                'afspraken': section_text(page, 'afspraken'),
            },
        })

    # ======================================
    # GROEI & DISPENSATIE JEUGD
    # ======================================
    if page == "groei":
        groei_tab = (request.GET.get("tab") or "groei").strip().lower()
        if groei_tab not in {"groei", "dispensaties", "bio-leeftijd", "geboortemaandeffect", "verjaardagen"}:
            groei_tab = "groei"

        selected_player_id = request.GET.get("player_id")
        if not selected_player_id:
            first_player = players.first()
            selected_player_id = str(first_player.id) if first_player else ""

        def parse_float(value):
            try:
                if value is None or value == "":
                    return None
                return float(value)
            except (TypeError, ValueError):
                return None

        def compute_maturity_offset(age, height, sitting_height, weight):
            if None in (age, height, sitting_height, weight) or height <= 0:
                return None
            leg_length = height - sitting_height
            return (
                -9.236
                + (0.0002708 * (leg_length * sitting_height))
                - (0.001663 * (age * leg_length))
                + (0.007216 * (age * sitting_height))
                + (0.02292 * ((weight / height) * 100))
            )

        if request.method == "POST":
            form_type = request.POST.get("form_type", "").strip()

            if form_type in {"growth_profile_save", "growth_measurement_add", "growth_measurement_delete"}:
                player_id = request.POST.get("player_id") or selected_player_id
                player = get_object_or_404(Player, id=player_id)
                profile, _ = GrowthProfile.objects.get_or_create(player=player)

                if form_type == "growth_profile_save":
                    profile.age = parse_float(request.POST.get("age"))
                    profile.height = parse_float(request.POST.get("height"))
                    profile.sitting_height = parse_float(request.POST.get("sitting_height"))
                    profile.weight = parse_float(request.POST.get("weight"))
                    profile.growth_complaints = request.POST.get("growth_complaints") == "on"
                    profile.action = (request.POST.get("action") or "").strip()
                    profile.maturity_offset = compute_maturity_offset(
                        profile.age, profile.height, profile.sitting_height, profile.weight
                    )
                    profile.save()
                    messages.success(request, "Groeiprofiel opgeslagen.")

                if form_type == "growth_measurement_add":
                    raw_date = request.POST.get("measurement_date") or ""
                    raw_height = request.POST.get("measurement_height")
                    measurement_height = parse_float(raw_height)

                    try:
                        measurement_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                    except ValueError:
                        measurement_date = None

                    if measurement_date and measurement_height is not None:
                        GrowthMeasurement.objects.update_or_create(
                            profile=profile,
                            date=measurement_date,
                            defaults={"height_cm": measurement_height},
                        )
                        messages.success(request, "Meetpunt opgeslagen.")
                    else:
                        messages.error(request, "Vul een geldige datum en lengte in.")

                if form_type == "growth_measurement_delete":
                    measurement_id = request.POST.get("measurement_id")
                    measurement = get_object_or_404(GrowthMeasurement, id=measurement_id, profile=profile)
                    measurement.delete()
                    messages.success(request, "Meetpunt verwijderd.")

                return redirect(f"/overig/?page=groei&tab={groei_tab}&player_id={player.id}")

            section = request.POST.get("section")
            text = request.POST.get("text", "")
            if section:
                OverigNote.objects.create(
                    note_type="section",
                    page_key="groei",
                    section_key=section,
                    text=text.strip(),
                )
            return redirect(f"/overig/?page=groei&tab={groei_tab}&player_id={selected_player_id}")

        selected_player = Player.objects.filter(id=selected_player_id).first()
        growth_profile = None
        growth_measurements = []
        growth_rate = None

        if selected_player:
            growth_profile = GrowthProfile.objects.filter(player=selected_player).first()
            if growth_profile:
                growth_measurements = list(growth_profile.measurements.all().order_by("date", "id"))
                if len(growth_measurements) >= 2:
                    first = growth_measurements[0]
                    last = growth_measurements[-1]
                    day_diff = (last.date - first.date).days
                    if day_diff > 0:
                        growth_rate = ((last.height_cm - first.height_cm) / day_diff) * 365.25

        return render(request, 'overig.html', {
            'page': 'groei',
            'groei_tab': groei_tab,
            'selected_player_id': selected_player.id if selected_player else None,
            'growth_profile': growth_profile,
            'growth_measurements': growth_measurements,
            'growth_rate': growth_rate,
            'players': players,
            'staff': staff_members,
            "groei_texts": {
                "beleid": section_text("groei", "beleid"),
                "casussen": section_text("groei", "casussen"),
                "afspraken": section_text("groei", "afspraken"),
            },
        })

    # ======================================
    # BEGELEIDING STAGIAIR(E)
    # ======================================
    if page == "stagiair":
        if request.method == "POST":
            section = request.POST.get("section")
            text = request.POST.get("text", "")
            if section:
                OverigNote.objects.create(
                    note_type="section",
                    page_key="stagiair",
                    section_key=section,
                    text=text.strip(),
                )
            return redirect("/overig/?page=stagiair")

        return render(request, 'overig.html', {
            'page': 'stagiair',
            'players': players,
            'staff': staff_members,
            "stagiair_texts": {
                "doelen": section_text("stagiair", "doelen"),
                "actie": section_text("stagiair", "actie"),
                "afspraken": section_text("stagiair", "afspraken"),
                "ambitie": section_text("stagiair", "ambitie"),
            },
        })

    # ======================================
    # VAKANTIEPROGRAMMA
    # ======================================
    if page == "vakantie":
        edit_id = request.GET.get("edit_id")
        if request.method == "POST":
            form_type = request.POST.get("form_type", "")

            if form_type == "vakantie_entry":
                player_id = request.POST.get("player_id")
                raw_date = request.POST.get("date") or ""
                loopvorm = request.POST.get("loopvorm", "").strip()
                kracht = request.POST.get("kracht", "").strip()
                completed = request.POST.get("completed") == "on"

                if not player_id or not raw_date:
                    messages.error(request, "Speler en datum zijn verplicht.")
                    return redirect("/overig/?page=vakantie")

                try:
                    entry_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:
                    messages.error(request, "Ongeldige datum. Gebruik het datumveld.")
                    return redirect("/overig/?page=vakantie")

                created_count = 0
                skipped_count = 0

                if player_id == "all":
                    players_qs = Player.objects.all()
                else:
                    players_qs = [get_object_or_404(Player, id=player_id)]

                for player in players_qs:
                    exists = VakantieProgrammaEntry.objects.filter(
                        player=player,
                        date=entry_date,
                        loopvorm=loopvorm,
                        kracht=kracht,
                    ).exists()
                    if exists:
                        skipped_count += 1
                        continue

                    VakantieProgrammaEntry.objects.create(
                        player=player,
                        date=entry_date,
                        loopvorm=loopvorm,
                        kracht=kracht,
                        completed=completed,
                    )
                    created_count += 1

                if created_count:
                    messages.success(request, f"Vakantieprogramma toegevoegd ({created_count} item(s)).")
                if skipped_count:
                    messages.warning(request, f"{skipped_count} item(s) bestonden al en zijn overgeslagen.")
                return redirect("/overig/?page=vakantie")

            if form_type == "vakantie_toggle":
                entry_id = request.POST.get("entry_id")
                entry = get_object_or_404(VakantieProgrammaEntry, id=entry_id)
                entry.completed = request.POST.get("completed") == "on"
                entry.save(update_fields=["completed"])
                return redirect("/overig/?page=vakantie")

            if form_type == "vakantie_update":
                entry_id = request.POST.get("entry_id")
                entry = get_object_or_404(VakantieProgrammaEntry, id=entry_id)

                raw_date = request.POST.get("date") or ""
                loopvorm = request.POST.get("loopvorm", "").strip()
                kracht = request.POST.get("kracht", "").strip()
                completed = request.POST.get("completed") == "on"

                try:
                    entry_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:
                    messages.error(request, "Ongeldige datum. Gebruik het datumveld.")
                    return redirect("/overig/?page=vakantie")

                entry.date = entry_date
                entry.loopvorm = loopvorm
                entry.kracht = kracht
                entry.completed = completed
                entry.save(update_fields=["date", "loopvorm", "kracht", "completed"])
                messages.success(request, "Vakantieprogramma bijgewerkt.")
                return redirect("/overig/?page=vakantie")

            if form_type == "vakantie_planning_create":
                raw_date = request.POST.get("date") or ""
                raw_visible_from = request.POST.get("visible_from") or ""
                loopvorm = request.POST.get("loopvorm", "").strip()
                kracht = request.POST.get("kracht", "").strip()
                direct_visible = request.POST.get("direct_visible") == "on"
                player_ids = request.POST.getlist("player_ids")

                if not raw_date or not raw_visible_from:
                    messages.error(request, "Datum en zichtbaar-vanaf zijn verplicht.")
                    return redirect("/overig/?page=vakantie")

                try:
                    plan_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                    visible_from = datetime.strptime(raw_visible_from, "%Y-%m-%d").date()
                except ValueError:
                    messages.error(request, "Ongeldige datum. Gebruik het datumveld.")
                    return redirect("/overig/?page=vakantie")

                if not player_ids:
                    messages.error(request, "Selecteer minimaal ÃƒÆ’Ã‚Â©ÃƒÆ’Ã‚Â©n speler.")
                    return redirect("/overig/?page=vakantie")

                if "all" in player_ids:
                    players_qs = Player.objects.all()
                else:
                    players_qs = Player.objects.filter(id__in=player_ids)

                if not players_qs.exists():
                    messages.error(request, "Geen geldige spelers geselecteerd.")
                    return redirect("/overig/?page=vakantie")

                planning = VakantiePlanning.objects.create(
                    date=plan_date,
                    loopvorm=loopvorm,
                    kracht=kracht,
                    visible_from=visible_from,
                    is_visible=direct_visible,
                )
                planning.players.set(players_qs)

                created_count = 0
                skipped_count = 0
                if direct_visible:
                    for player in players_qs:
                        exists = VakantieProgrammaEntry.objects.filter(
                            player=player,
                            date=plan_date,
                            loopvorm=loopvorm,
                            kracht=kracht,
                        ).exists()
                        if exists:
                            skipped_count += 1
                            continue
                        VakantieProgrammaEntry.objects.create(
                            player=player,
                            date=plan_date,
                            loopvorm=loopvorm,
                            kracht=kracht,
                            completed=False,
                        )
                        created_count += 1

                messages.success(request, "Planning toegevoegd.")
                if direct_visible and created_count:
                    messages.success(request, f"Zichtbaar gemaakt ({created_count} item(s)).")
                if direct_visible and skipped_count:
                    messages.warning(request, f"{skipped_count} item(s) bestonden al en zijn overgeslagen.")
                return redirect("/overig/?page=vakantie")

            if form_type == "vakantie_planning_publish":
                planning_id = request.POST.get("planning_id")
                planning = get_object_or_404(VakantiePlanning, id=planning_id)
                players_qs = planning.players.all()

                created_count = 0
                skipped_count = 0
                for player in players_qs:
                    exists = VakantieProgrammaEntry.objects.filter(
                        player=player,
                        date=planning.date,
                        loopvorm=planning.loopvorm or "",
                        kracht=planning.kracht or "",
                    ).exists()
                    if exists:
                        skipped_count += 1
                        continue
                    VakantieProgrammaEntry.objects.create(
                        player=player,
                        date=planning.date,
                        loopvorm=planning.loopvorm,
                        kracht=planning.kracht,
                        completed=False,
                    )
                    created_count += 1

                planning.is_visible = True
                planning.save(update_fields=["is_visible"])

                messages.success(request, "Planning zichtbaar gemaakt.")
                if created_count:
                    messages.success(request, f"{created_count} item(s) toegevoegd.")
                if skipped_count:
                    messages.warning(request, f"{skipped_count} item(s) bestonden al en zijn overgeslagen.")
                return redirect("/overig/?page=vakantie")

            section = request.POST.get("section")
            text = request.POST.get("text", "")
            if section:
                OverigNote.objects.create(
                    note_type="section",
                    page_key="vakantie",
                    section_key=section,
                    text=text.strip(),
                )
            return redirect("/overig/?page=vakantie")

        vakantie_entries = (
            VakantieProgrammaEntry.objects
            .select_related("player")
            .order_by("-date", "player__name")
        )
        vakantie_planningen = (
            VakantiePlanning.objects
            .prefetch_related("players")
            .order_by("-date", "-created_at")
        )

        return render(request, 'overig.html', {
            'page': 'vakantie',
            'players': players,
            'staff': staff_members,
            "edit_id": int(edit_id) if edit_id and edit_id.isdigit() else None,
            "vakantie_entries": vakantie_entries,
            "vakantie_planningen": vakantie_planningen,
            "vakantie_texts": {
                "doelen": section_text("vakantie", "doelen"),
                "schema": section_text("vakantie", "schema"),
                "afspraken": section_text("vakantie", "afspraken"),
                "monitoring": section_text("vakantie", "monitoring"),
            },
        })

    # ======================================
    # DEFAULT ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ MENU
    # ======================================
    return render(request, 'overig.html', {
        'page': 'menu',
        'players': players,
        'staff': staff_members,
    })


def beleid(request):
    beleid_tab = (request.GET.get("tab") or "voetbalbeleid").strip().lower()
    if beleid_tab not in {"voetbalbeleid", "fysiek-beleid", "beleid-jeugd"}:
        beleid_tab = "voetbalbeleid"

    subtab_options = {
        "voetbalbeleid": ["speelwijze", "teamafspraken"],
        "fysiek-beleid": ["voeding", "krachttraining", "testen-meten", "leefstijl"],
        "beleid-jeugd": ["onderbouw", "middenbouw", "bovenbouw"],
    }
    beleid_subtab = (request.GET.get("subtab") or subtab_options[beleid_tab][0]).strip().lower()
    if beleid_subtab not in subtab_options[beleid_tab]:
        beleid_subtab = subtab_options[beleid_tab][0]

    section_key = f"{beleid_tab}:{beleid_subtab}"

    def section_text(section_key: str) -> str:
        item = (
            OverigNote.objects
            .filter(note_type="section", page_key="beleid", section_key=section_key)
            .order_by("-created_at")
            .first()
        )
        return (item.text or "") if item else ""

    def section_images(section_key: str):
        return BeleidSectionImage.objects.filter(
            page_key="beleid",
            section_key=section_key,
        ).order_by("-created_at")

    if request.method == "POST":
        section = request.POST.get("section", "").strip()
        text = request.POST.get("text", "")
        if section:
            OverigNote.objects.create(
                note_type="section",
                page_key="beleid",
                section_key=section,
                text=text.strip(),
            )
            for image in request.FILES.getlist("images"):
                if image:
                    BeleidSectionImage.objects.create(
                        page_key="beleid",
                        section_key=section,
                        image=image,
                    )
            messages.success(request, "Succesvol opgeslagen.")
        return redirect(f"/beleid/?tab={beleid_tab}&subtab={beleid_subtab}")

    return render(request, "beleid.html", {
        "beleid_tab": beleid_tab,
        "beleid_subtab": beleid_subtab,
        "beleid_current_text": section_text(section_key),
        "beleid_images": section_images(section_key),
    })


@login_required
@role_required(ROLE_ADMIN)
def staf(request):
    staff_members = Staff.objects.select_related("role_ref", "user").all().order_by("name")
    players = list(
        Player.objects
        .select_related("position_ref")
        .prefetch_related("team_assignments__team")
        .all()
        .order_by("name")
    )
    staff_roles = StaffRole.objects.filter(is_active=True).order_by("name")
    player_positions = PlayerPosition.objects.filter(is_active=True).order_by("name")
    dashboard_roles = _dashboard_role_values()
    player_team_options = _academy_team_options()

    def current_player_team(player):
        today = timezone.localdate()
        assignments = [
            assignment
            for assignment in player.team_assignments.all()
            if assignment.start_date <= today and (assignment.end_date is None or assignment.end_date >= today)
        ]
        if assignments:
            assignment = sorted(assignments, key=lambda item: item.start_date, reverse=True)[0]
            return assignment.team
        if not player.is_active:
            return Team.objects.filter(code__iexact="OUD").first()
        return None

    def sync_player_team(player, team_code):
        team_code = (team_code or "").strip().upper()
        if not team_code:
            return
        if team_code == "OUD":
            team, _ = Team.objects.get_or_create(code="OUD", defaults={"name": "Oud spelers"})
            if team.name != "Oud spelers":
                team.name = "Oud spelers"
                team.save(update_fields=["name"])
            player.is_active = False
            player.save(update_fields=["is_active"])
        else:
            team, _ = Team.objects.get_or_create(code=team_code, defaults={"name": team_code})
            if team.name != team_code:
                team.name = team_code
                team.save(update_fields=["name"])
            player.is_active = True
            player.save(update_fields=["is_active"])

        today = timezone.localdate()
        PlayerTeamAssignment.objects.filter(
            player=player,
            end_date__isnull=True,
        ).exclude(team=team).update(end_date=today - timedelta(days=1))
        PlayerTeamAssignment.objects.filter(
            player=player,
            end_date__gte=today,
        ).exclude(team=team).update(end_date=today - timedelta(days=1))
        assignment, created = PlayerTeamAssignment.objects.get_or_create(
            player=player,
            team=team,
            start_date=today,
            defaults={"end_date": None},
        )
        if not created and assignment.end_date is not None:
            assignment.end_date = None
            assignment.save(update_fields=["end_date"])

    if request.method == "POST":
        form_type = (request.POST.get("form_type") or "").strip()

        if form_type == "add_player":
            name = (request.POST.get("player_name") or "").strip()
            position_name = (request.POST.get("position_name") or "").strip()
            team_code = (request.POST.get("team_code") or "").strip().upper()
            image = request.FILES.get("player_image")

            if not name:
                messages.error(request, "Vul een spelernaam in.")
                return redirect("staf")
            if not team_code:
                messages.error(request, "Kies een team voor deze speler.")
                return redirect("staf")
            if team_code and team_code not in _academy_codes():
                messages.error(request, "Kies een geldig team voor deze speler.")
                return redirect("staf")
            if Player.objects.filter(name__iexact=name).exists():
                messages.error(request, f"Speler {name} bestaat al.")
                return redirect("staf")

            position_obj = None
            if position_name:
                position_obj, _ = PlayerPosition.objects.get_or_create(name=position_name)

            player = Player.objects.create(
                name=name,
                position_ref=position_obj,
                image=image if image else None,
                is_active=True,
            )
            sync_player_team(player, team_code)
            PlayerMonitoringProfile.objects.get_or_create(player=player)
            _record_audit(
                request,
                action="toegevoegd",
                category="Speler",
                object_label=player.name,
                details=f"Speler toegevoegd aan {_academy_team_label(team_code)}.",
            )
            messages.success(request, f"Succesvol opgeslagen. Speler {player.name} toegevoegd.")
            return redirect("staf")

        if form_type == "edit_player":
            player = get_object_or_404(Player.objects.select_related("position_ref"), id=request.POST.get("player_id"))
            name = (request.POST.get("player_name") or "").strip()
            position_name = (request.POST.get("position_name") or "").strip()
            team_code = (request.POST.get("team_code") or "").strip().upper()
            image = request.FILES.get("player_image")

            if not name:
                messages.error(request, "Vul een spelernaam in.")
                return redirect("staf")
            if not team_code:
                messages.error(request, "Kies een team voor deze speler.")
                return redirect("staf")
            if team_code and team_code not in _academy_codes():
                messages.error(request, "Kies een geldig team voor deze speler.")
                return redirect("staf")
            if Player.objects.exclude(id=player.id).filter(name__iexact=name).exists():
                messages.error(request, f"Speler {name} bestaat al.")
                return redirect("staf")

            position_obj = None
            if position_name:
                position_obj, _ = PlayerPosition.objects.get_or_create(name=position_name)

            player.name = name
            player.position_ref = position_obj
            player.is_active = request.POST.get("is_active") == "on"
            if image:
                player.image = image
            player.save()
            sync_player_team(player, team_code)
            PlayerMonitoringProfile.objects.get_or_create(player=player)
            _record_audit(
                request,
                action="bijgewerkt",
                category="Speler",
                object_label=player.name,
                details=f"Spelergegevens bijgewerkt. Team: {_academy_team_label(team_code)}.",
            )
            messages.success(request, f"Succesvol opgeslagen. Speler {player.name} bijgewerkt.")
            return redirect("staf")

        if form_type == "add_staff":
            name = (request.POST.get("name") or "").strip()
            role_name = (request.POST.get("role_name") or "").strip()
            image = request.FILES.get("image")
            username = (request.POST.get("username") or "").strip()
            email = (request.POST.get("email") or "").strip()
            password = request.POST.get("password") or ""
            dashboard_role = (request.POST.get("dashboard_role") or "").strip()

            if not name or not role_name:
                messages.error(request, "Vul zowel naam als functie in.")
                return redirect("staf")
            if dashboard_role and dashboard_role not in dashboard_roles:
                messages.error(request, "Kies een geldige dashboardrol.")
                return redirect("staf")

            try:
                with transaction.atomic():
                    user = None
                    if username:
                        User = get_user_model()
                        user, created = User.objects.get_or_create(
                            username=username,
                            defaults={
                                "email": email,
                                "first_name": name.split(" ", 1)[0],
                                "last_name": name.split(" ", 1)[1] if " " in name else "",
                            },
                        )
                        if email and user.email != email:
                            user.email = email
                        if password:
                            user.set_password(password)
                        elif created:
                            user.set_unusable_password()
                        user.is_staff = dashboard_role == ROLE_ADMIN
                        user.is_active = True
                        user.save()
                        _sync_user_dashboard_role(user, dashboard_role)

                role_obj, _ = StaffRole.objects.get_or_create(name=role_name)
                Staff.objects.create(
                    name=name,
                    role_ref=role_obj,
                    image=image if image else None,
                    user=user,
                )
                _record_audit(
                    request,
                    action="toegevoegd",
                    category="Staf",
                    object_label=name,
                    details=f"Staflid toegevoegd met rol: {role_name}.",
                )
                messages.success(request, "Succesvol opgeslagen. Staflid toegevoegd.")
            except Exception:
                messages.error(
                    request,
                    "Uploaden van de foto is mislukt. Gebruik bij voorkeur een JPG, PNG of WEBP-bestand en probeer opnieuw.",
                )
            return redirect("staf")

        if form_type == "edit_staff":
            staff_member = get_object_or_404(Staff.objects.select_related("user"), id=request.POST.get("staff_id"))
            name = (request.POST.get("name") or "").strip()
            role_name = (request.POST.get("role_name") or "").strip()
            image = request.FILES.get("image")
            username = (request.POST.get("username") or "").strip()
            email = (request.POST.get("email") or "").strip()
            password = request.POST.get("password") or ""
            dashboard_role = (request.POST.get("dashboard_role") or "").strip()
            is_active = request.POST.get("is_active") == "on"

            if not name or not role_name:
                messages.error(request, "Vul zowel naam als functie in.")
                return redirect("staf")
            if dashboard_role and dashboard_role not in dashboard_roles:
                messages.error(request, "Kies een geldige dashboardrol.")
                return redirect("staf")
            if dashboard_role and not username:
                messages.error(request, "Vul een gebruikersnaam in om een dashboardrol te koppelen.")
                return redirect("staf")

            try:
                with transaction.atomic():
                    role_obj, _ = StaffRole.objects.get_or_create(name=role_name)
                    staff_member.name = name
                    staff_member.role_ref = role_obj
                    if image:
                        staff_member.image = image

                    user = staff_member.user
                    if username:
                        User = get_user_model()
                        matching_user = User.objects.filter(username=username).first()
                        if user and matching_user and matching_user.id != user.id:
                            messages.error(request, f"Gebruikersnaam {username} is al in gebruik.")
                            return redirect("staf")
                        if user is None:
                            if matching_user and hasattr(matching_user, "staff_profile"):
                                messages.error(request, f"Gebruikersnaam {username} is al gekoppeld aan een ander staflid.")
                                return redirect("staf")
                            user = matching_user or User(username=username)
                        user.username = username
                        user.email = email
                        user.first_name = name.split(" ", 1)[0]
                        user.last_name = name.split(" ", 1)[1] if " " in name else ""
                        if password:
                            user.set_password(password)
                        elif user.pk is None:
                            user.set_unusable_password()
                        user.is_active = is_active
                        user.save()
                        _sync_user_dashboard_role(user, dashboard_role)
                        staff_member.user = user
                    elif user:
                        user.email = email
                        user.first_name = name.split(" ", 1)[0]
                        user.last_name = name.split(" ", 1)[1] if " " in name else ""
                        if password:
                            user.set_password(password)
                        user.is_active = is_active
                        user.save()
                        _sync_user_dashboard_role(user, dashboard_role)

                    staff_member.save()
                _record_audit(
                    request,
                    action="bijgewerkt",
                    category="Staf",
                    object_label=staff_member.name,
                    details=f"Stafprofiel bijgewerkt. Rol: {role_name}. Dashboardrol: {_dashboard_role_label(dashboard_role) or 'geen'}.",
                )
                messages.success(request, "Succesvol opgeslagen. Staflid bijgewerkt.")
            except Exception:
                messages.error(
                    request,
                    "Staflid bijwerken is mislukt. Controleer de gegevens en probeer opnieuw.",
                )
            return redirect("staf")

        if form_type == "delete_staff":
            staff_member = get_object_or_404(Staff.objects.select_related("user"), id=request.POST.get("staff_id"))
            staff_name = staff_member.name
            linked_user = staff_member.user

            if linked_user and linked_user.pk == request.user.pk:
                messages.error(request, "Je kunt je eigen ingelogde account niet via deze pagina verwijderen.")
                return redirect("staf")

            try:
                with transaction.atomic():
                    _record_audit(
                        request,
                        action="verwijderd",
                        category="Staf",
                        object_label=staff_name,
                        details="Stafprofiel en gekoppelde login verwijderd.",
                    )
                    staff_member.delete()
                    if linked_user:
                        linked_user.delete()
                messages.success(request, f"Staflid {staff_name} is verwijderd en de toegang is ingetrokken.")
            except Exception:
                messages.error(request, "Staflid verwijderen is mislukt. Probeer het opnieuw.")
            return redirect("staf")

        messages.error(request, "Onbekend formulier.")
        return redirect("staf")

    staff_member_rows = []
    for player in players:
        team = current_player_team(player)
        player.current_team_code = team.code if team else ""
        player.current_team_label = _academy_team_label(team.code) if team else "Geen team gekoppeld"

    staff_user_ids = [member.user_id for member in staff_members if member.user_id]
    audit_logs_by_user_id = {user_id: [] for user_id in staff_user_ids}
    if staff_user_ids:
        for log in AuditLog.objects.filter(actor_id__in=staff_user_ids).select_related("actor").order_by("actor_id", "-created_at"):
            logs = audit_logs_by_user_id.setdefault(log.actor_id, [])
            if len(logs) < 8:
                logs.append(log)

    for member in staff_members:
        dashboard_role = _user_dashboard_role(member.user)
        staff_member_rows.append(
            SimpleNamespace(
                member=member,
                dashboard_role=dashboard_role,
                dashboard_role_label=_dashboard_role_label(dashboard_role),
                audit_logs=audit_logs_by_user_id.get(member.user_id, []),
            )
        )

    return render(request, "staf.html", {
        "staff_members": staff_members,
        "staff_member_rows": staff_member_rows,
        "players": players,
        "staff_roles": staff_roles,
        "player_positions": player_positions,
        "player_team_options": player_team_options,
        "dashboard_role_choices": ROLE_CHOICES,
    })


def player_data(request, player_id):
    """
    Geeft JSON terug met de voortgang van gewicht en huidplooien
    voor ??n specifieke speler. Wordt aangeroepen als je op een speler klikt.
    """
    from .models import Player
    _require_own_player_for_player_user(request, player_id)

    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({'error': 'Speler niet gevonden'}, status=404)

    tests = [r for r in fetch_performance_rows("test") if r["player_id"] == player.id]
    tests.sort(key=lambda r: r["session_date"])

    if not tests:
        profile = getattr(player, "monitoring_profile", None)
        prev_weight = float(profile.prev_weight or 0) if profile and profile.prev_weight is not None else 0.0
        curr_weight = float(profile.curr_weight or 0) if profile and profile.curr_weight is not None else 0.0
        skinfold = float(profile.sum_skinfolds or 0) if profile and profile.sum_skinfolds is not None else 0.0
        data = {
            'dates': ["Week 1", "Week 2", "Week 3", "Week 4"],
            'weights': [
                prev_weight,
                float(prev_weight * 0.99),
                curr_weight,
                float(curr_weight * 1.01),
            ],
            'skinfolds': [
                skinfold,
                float(skinfold * 0.98),
                skinfold,
                float(skinfold * 1.02),
            ]
        }
        return JsonResponse(data)

    dates = [t["session_date"].strftime("%d-%m-%Y") for t in tests]
    weights = [float(t.get("curr_weight") or 0) for t in tests]
    skinfolds = [float(t.get("sum_skinfolds") or 0) for t in tests]

    data = {
        'dates': dates,
        'weights': weights,
        'skinfolds': skinfolds
    }
    return JsonResponse(data)

    # ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Echte data gebruiken uit PlayerTest
    dates = [t.created_at.strftime("%d-%m-%Y") for t in tests]
    weights = [float(t.curr_weight or 0) for t in tests]
    skinfolds = [float(t.sum_skinfolds or 0) for t in tests]

    data = {
        'dates': dates,
        'weights': weights,
        'skinfolds': skinfolds
    }
    return JsonResponse(data)


def weight_data(request, player_id):
    """
    JSON met gewichtstrend voor een speler.
    """
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({'error': 'Speler niet gevonden'}, status=404)

    entries = WeightEntry.objects.filter(player=player).order_by("date")
    if not entries.exists():
        dates = []
        weights = []
        profile = getattr(player, "monitoring_profile", None)
        if profile and profile.prev_weight is not None:
            dates.append("Vorige")
            weights.append(float(profile.prev_weight))
        if profile and profile.curr_weight is not None:
            dates.append("Huidig")
            weights.append(float(profile.curr_weight))
        return JsonResponse({"dates": dates, "weights": weights})

    dates = [e.date.strftime("%d-%m-%Y") for e in entries]
    weights = [float(e.weight) for e in entries]
    return JsonResponse({"dates": dates, "weights": weights})
    
# ---------- DATA-UPLOAD (CSV) ----------
from django.shortcuts import redirect
from django.contrib import messages
import csv
from datetime import datetime
import unicodedata


GPS_TRAINING_METRICS = {
    "total_distance": ("Total Distance", "m", "distance"),
    "hsd": ("HIR (M>20 KM/U)", "m", "speed"),
    "sprints": ("Sprints", "", "speed"),
    "load": ("Load", "au", "load"),
}

GPS_MATCH_METRICS = {
    "accelerations": ("Accelerations", "", "intensity"),
    "decelerations": ("Decelerations", "", "intensity"),
    "hsd": ("HIR (M>20 KM/U)", "m", "speed"),
    "his": ("HIS (M>25 KM/U)", "m", "speed"),
    "total_distance": ("Total Distance", "m", "distance"),
    "sprints": ("Sprints", "", "speed"),
    "load": ("HML Distance", "m", "load"),
    "first_half_load": ("Load eerste helft", "au", "load"),
    "second_half_load": ("Load tweede helft", "au", "load"),
}

GPS_UPLOAD_EVENTS = {
    "opstart_training": ("Opstart training", "training"),
    "sneller_herstellen": ("Sneller herstellen", "training"),
    "volhouden_herstellen": ("Volhouden herstellen", "training"),
    "competitiewedstrijd": ("Competitiewedstrijd", "match"),
}


def _decode_uploaded_csv(uploaded_file):
    raw = uploaded_file.read()
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding).splitlines()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("csv", raw, 0, 1, "CSV kon niet worden gelezen")


def _normalize_csv_value(value):
    return str(value or "").replace('"', "").strip()


def _normalize_name(value):
    normalized = unicodedata.normalize("NFKD", _normalize_csv_value(value).lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _csv_float(value):
    cleaned = _normalize_csv_value(value)
    if not cleaned:
        return 0.0
    cleaned = cleaned.replace(" ", "")
    if "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _csv_float_or_none(value):
    cleaned = _normalize_csv_value(value)
    if not cleaned:
        return None
    cleaned = cleaned.replace(" ", "")
    if "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def _csv_int(value):
    try:
        return int(round(_csv_float(value)))
    except (TypeError, ValueError):
        return 0


def _csv_int_or_none(value):
    value = _csv_float_or_none(value)
    if value is None:
        return None
    return int(round(value))


def _csv_get(row, column_name):
    wanted = (column_name or "").strip().lower()
    for key, value in row.items():
        if str(key or "").strip().lower() == wanted:
            return value
    return None


def _parse_statsports_date(value):
    cleaned = _normalize_csv_value(value)
    for date_format in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(cleaned, date_format).date()
        except ValueError:
            continue
    return None


def _csv_has_columns(reader, required_columns):
    fieldnames = {str(field or "").strip().lower() for field in (reader.fieldnames or [])}
    return all(column.lower() in fieldnames for column in required_columns)


def _csv_has_any_column(reader, column_names):
    fieldnames = {str(field or "").strip().lower() for field in (reader.fieldnames or [])}
    return any(column.lower() in fieldnames for column in column_names)


def _ensure_gps_metric_types(metric_map):
    for code, (label, unit, category) in metric_map.items():
        PerformanceMetricType.objects.get_or_create(
            code=code,
            defaults={"label": label, "unit": unit, "category": category, "is_active": True},
        )


def _find_player_from_gps_lastname(players, csv_lastname, *, allow_contains=False):
    normalized_lastname = _normalize_name(csv_lastname)
    if not normalized_lastname:
        return None
    for player in players:
        player_name = _normalize_name(player.name)
        player_lastname = player_name.split()[-1] if player_name.split() else ""
        if player_lastname == normalized_lastname:
            return player
        if allow_contains and normalized_lastname in player_name:
            return player
    return None


def _team_players_for_gps_upload(team_code):
    team_code = _normalize_csv_value(team_code).upper()
    if team_code in {"OUD SPELERS", "OUD-SPELERS", "OUD"}:
        team_code = "OUD"
    team = Team.objects.filter(Q(code__iexact=team_code) | Q(name__iexact=team_code), is_active=True).first()
    if not team and team_code != "OUD":
        return None, Player.objects.none()
    today = timezone.localdate()
    if team_code == "OUD":
        assigned_old_players = Player.objects.none()
        if team:
            assigned_old_players = (
                Player.objects
                .filter(team_assignments__team=team)
                .filter(Q(team_assignments__end_date__isnull=True) | Q(team_assignments__end_date__gte=today))
            )
        players = (
            Player.objects
            .filter(Q(is_active=False) | Q(id__in=assigned_old_players.values("id")))
            .distinct()
            .order_by("name")
        )
    else:
        players = (
            Player.objects
            .filter(is_active=True, team_assignments__team=team)
            .filter(Q(team_assignments__end_date__isnull=True) | Q(team_assignments__end_date__gte=today))
            .distinct()
            .order_by("name")
        )
    return team, players


def _gps_upload_selection(request):
    team_code = _normalize_csv_value(request.POST.get("upload_team"))
    event_code = _normalize_csv_value(request.POST.get("upload_event"))
    if not team_code:
        messages.error(request, "Kies eerst een team voor de GPS-upload.")
        return None
    if event_code not in GPS_UPLOAD_EVENTS:
        messages.error(request, "Kies eerst een geldig event voor de GPS-upload.")
        return None
    team, players = _team_players_for_gps_upload(team_code)
    if not team and team_code.upper() not in {"OUD", "OUD SPELERS", "OUD-SPELERS"}:
        messages.error(request, f"Team {team_code} is niet gevonden.")
        return None
    is_old_players_team = team_code.upper() in {"OUD", "OUD SPELERS", "OUD-SPELERS"}
    team_label = _academy_team_label("OUD") if is_old_players_team else team.name
    if not players.exists():
        messages.error(request, f"{team_label} heeft nog geen spelers. Koppel eerst spelers aan dit team of archiveer oude spelers.")
        return None
    event_label, session_kind = GPS_UPLOAD_EVENTS[event_code]
    return {
        "team": team,
        "team_code": "OUD" if is_old_players_team else team.code,
        "team_label": team_label,
        "players": list(players),
        "event_code": event_code,
        "event_label": event_label,
        "session_kind": session_kind,
    }


def _gps_session_exists(player, session_kind, session_date, source_tag=None):
    kind = PerformanceSessionKind.objects.filter(code=session_kind).first()
    if not kind:
        return False
    qs = PerformanceSession.objects.filter(
        player=player,
        session_kind_ref=kind,
        session_date=session_date,
    )
    if source_tag:
        qs = qs.filter(source_legacy_table=source_tag, source_legacy_id=0)
    return qs.exists()


def _show_gps_import_feedback(request, *, imported, duplicates, skipped, invalid_dates, unknown_players, missing_values, label):
    if imported:
        messages.success(request, f"Succesvol opgeslagen. {imported} {label}regels geïmporteerd.")
    elif duplicates and not (skipped or invalid_dates or unknown_players):
        messages.error(request, f"Geen nieuwe {label}regels geïmporteerd. Dit bestand of deze speler-datum-event combinatie lijkt al eerder verwerkt.")
    else:
        messages.error(request, f"Er zijn geen {label}regels geïmporteerd.")
    if duplicates:
        messages.error(
            request,
            f"{duplicates} dubbele {label}regel(s) overgeslagen. Deze speler-datum-event combinatie bestaat al of stond dubbel in het bestand.",
        )
    if invalid_dates or unknown_players or skipped or missing_values:
        messages.warning(
            request,
            f"Controleer je CSV: {invalid_dates} ongeldige datum(s), {unknown_players} onbekende speler(s), {skipped} lege/onvolledige rij(en) overgeslagen, {missing_values} lege/ongeldige meetwaarde(n) genegeerd.",
        )


def _import_log_status(*, processed_count, duplicate_count=0, error_count=0):
    if processed_count and not duplicate_count and not error_count:
        return "success"
    if processed_count:
        return "partial"
    return "failed"


def _add_import_detail(details, message, limit=20):
    if len(details) < limit:
        details.append(message)


def _import_detail(problem, *, row=None, action="", value="", field=""):
    detail = {
        "problem": problem,
        "action": action or "Controleer deze regel en upload daarna het gecorrigeerde bestand opnieuw.",
    }
    if row:
        detail["row"] = row
    if value:
        detail["value"] = value
    if field:
        detail["field"] = field
    return detail


def _add_import_issue(details, problem, *, row=None, action="", value="", field="", limit=20):
    _add_import_detail(
        details,
        _import_detail(problem, row=row, action=action, value=value, field=field),
        limit=limit,
    )


def _record_data_import_log(
    request,
    *,
    data_type,
    filename="",
    upload_selection=None,
    status="failed",
    processed_count=0,
    duplicate_count=0,
    error_count=0,
    details=None,
):
    upload_selection = upload_selection or {}
    DataImportLog.objects.create(
        uploaded_by=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        data_type=data_type,
        team_code=upload_selection.get("team_code", ""),
        team_label=upload_selection.get("team_label", ""),
        event_code=upload_selection.get("event_code", ""),
        event_label=upload_selection.get("event_label", ""),
        filename=filename or "",
        status=status,
        processed_count=processed_count or 0,
        duplicate_count=duplicate_count or 0,
        error_count=error_count or 0,
        details=details or [],
    )


def _latest_admin_import_logs(request, limit=20):
    if not _is_admin_user(request.user):
        return []
    return DataImportLog.objects.select_related("uploaded_by").order_by("-created_at")[:limit]


def upload_file(request):
    """Uploadt een StatsSports CSV en schrijft trainingdata naar 3NF performance-tabellen."""
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        filename = csv_file.name or ""

        if not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Upload een geldig CSV-bestand (.csv).')
            _record_data_import_log(
                request,
                data_type="GPS",
                filename=filename,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Bestandstype is ongeldig.",
                        field="Bestand",
                        value=filename,
                        action="Upload een bestand met de extensie .csv.",
                    )
                ],
            )
            return redirect('training')
        upload_selection = _gps_upload_selection(request)
        if not upload_selection:
            _record_data_import_log(
                request,
                data_type="GPS",
                filename=filename,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Team, event of spelerslijst is niet geldig.",
                        action="Kies eerst een geldig team en event. Controleer ook of dit team spelers bevat.",
                    )
                ],
            )
            return redirect('training')
        if upload_selection["session_kind"] == "match":
            return upload_wedstrijddata(request)

        try:
            decoded_file = _decode_uploaded_csv(csv_file)
        except UnicodeDecodeError:
            messages.error(request, 'Het CSV-bestand kon niet worden gelezen. Exporteer het bestand opnieuw als CSV met UTF-8 of Windows-1252 encoding.')
            _record_data_import_log(
                request,
                data_type="GPS",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "CSV kon niet worden gelezen.",
                        action="Exporteer het bestand opnieuw als CSV met UTF-8 of Windows-1252 encoding.",
                    )
                ],
            )
            return redirect('training')

        reader = csv.DictReader(decoded_file, skipinitialspace=True)
        if not reader.fieldnames:
            messages.error(request, 'Het CSV-bestand bevat geen kolomkoppen.')
            _record_data_import_log(
                request,
                data_type="GPS",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "CSV bevat geen kolomkoppen.",
                        action="Zorg dat de eerste rij de kolomnamen bevat, zoals Player Last Name en Session Date.",
                    )
                ],
            )
            return redirect('training')
        if not _csv_has_columns(reader, ("Player Last Name", "Session Date")):
            missing_columns = [
                column for column in ("Player Last Name", "Session Date")
                if not _csv_has_columns(reader, (column,))
            ]
            messages.error(request, 'Het CSV-bestand mist verplichte kolommen: Player Last Name en Session Date.')
            _record_data_import_log(
                request,
                data_type="GPS",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Verplichte kolom ontbreekt.",
                        field=", ".join(missing_columns) or "Player Last Name / Session Date",
                        action="Voeg deze kolom toe aan de CSV-export en upload het bestand opnieuw.",
                    )
                ],
            )
            return redirect('training')
        if not _csv_has_any_column(reader, ("Total Distance", "HIR (M>20 KM/U)", "Sprints")):
            messages.error(request, 'Het CSV-bestand bevat geen herkenbare GPS-kolommen zoals Total Distance, HIR of Sprints.')
            _record_data_import_log(
                request,
                data_type="GPS",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Geen herkenbare GPS-meetkolommen gevonden.",
                        field="Total Distance / HIR (M>20 KM/U) / Sprints",
                        action="Controleer of de StatsSports-export minimaal een van deze GPS-kolommen bevat.",
                    )
                ],
            )
            return redirect('training')

        _ensure_gps_metric_types(GPS_TRAINING_METRICS)
        players = upload_selection["players"]
        csv_columns = {str(field or "").strip().lower() for field in (reader.fieldnames or [])}
        seen_sessions = set()
        count = 0
        duplicates = 0
        skipped = 0
        invalid_dates = 0
        unknown_players = 0
        missing_values = 0
        details = []
        source_tag = f"main_upload_training_{upload_selection['event_code']}"

        for row_number, row in enumerate(reader, start=2):
            csv_lastname = _normalize_csv_value(_csv_get(row, 'Player Last Name'))
            if not csv_lastname:
                skipped += 1
                _add_import_issue(
                    details,
                    "Spelernaam ontbreekt.",
                    row=row_number,
                    field="Player Last Name",
                    action="Vul in deze rij de achternaam/spelernaam in zoals die in het gekozen team staat.",
                )
                continue

            player = _find_player_from_gps_lastname(players, csv_lastname)
            if not player:
                unknown_players += 1
                _add_import_issue(
                    details,
                    "Speler niet gevonden binnen het gekozen team.",
                    row=row_number,
                    field="Player Last Name",
                    value=csv_lastname,
                    action=f"Controleer de spelling of kies het juiste team. Deze upload staat nu op {upload_selection['team_label']}.",
                )
                continue

            date_obj = _parse_statsports_date(_csv_get(row, 'Session Date'))
            if not date_obj:
                invalid_dates += 1
                _add_import_issue(
                    details,
                    "Datum ontbreekt of is ongeldig.",
                    row=row_number,
                    field="Session Date",
                    value=_normalize_csv_value(_csv_get(row, 'Session Date')),
                    action="Gebruik een geldige datum, bijvoorbeeld 15/05/2026 of 2026-05-15.",
                )
                continue

            session_key = (player.id, "training", date_obj, source_tag)
            if session_key in seen_sessions or _gps_session_exists(player, "training", date_obj, source_tag):
                duplicates += 1
                _add_import_issue(
                    details,
                    "Dubbele GPS-data gevonden.",
                    row=row_number,
                    value=f"{player.name} op {date_obj.strftime('%d-%m-%Y')}",
                    action="Deze speler-datum-event combinatie bestaat al. Verwijder de dubbele rij of kies een ander event als het om een andere sessie gaat.",
                )
                continue

            metric_columns = {
                'total_distance': ('Total Distance', _csv_float_or_none),
                'hsd': ('HIR (M>20 KM/U)', _csv_float_or_none),
                'sprints': ('Sprints', _csv_int_or_none),
                'load': ('Load', _csv_float_or_none),
            }
            valid_metrics = {}
            for code, (column_name, parser) in metric_columns.items():
                if column_name.lower() not in csv_columns:
                    continue
                value = parser(_csv_get(row, column_name))
                if value is None:
                    missing_values += 1
                else:
                    valid_metrics[code] = value
            if not valid_metrics:
                skipped += 1
                _add_import_issue(
                    details,
                    "Geen geldige GPS-meetwaarden gevonden.",
                    row=row_number,
                    field="Total Distance / HIR / Sprints / Load",
                    action="Vul minimaal een geldige meetwaarde in of controleer of de kolomnamen uit StatsSports kloppen.",
                )
                continue

            week = date_obj.isocalendar()[1]
            upsert_performance_session_metrics(
                player=player,
                session_kind='training',
                session_date=date_obj,
                week=week,
                metrics=valid_metrics,
                source_tag=source_tag,
                match_source=True,
            )
            seen_sessions.add(session_key)
            count += 1

        _show_gps_import_feedback(
            request,
            imported=count,
            duplicates=duplicates,
            skipped=skipped,
            invalid_dates=invalid_dates,
            unknown_players=unknown_players,
            missing_values=missing_values,
            label=f"{upload_selection['team_label']} {upload_selection['event_label'].lower()}",
        )
        error_count = skipped + invalid_dates + unknown_players + missing_values
        _record_data_import_log(
            request,
            data_type="GPS",
            filename=filename,
            upload_selection=upload_selection,
            status=_import_log_status(processed_count=count, duplicate_count=duplicates, error_count=error_count),
            processed_count=count,
            duplicate_count=duplicates,
            error_count=error_count,
            details=details,
        )
        return redirect('training')

    if request.method == 'POST':
        messages.error(request, 'Kies eerst een CSV-bestand om te uploaden.')
        _record_data_import_log(
            request,
            data_type="GPS",
            status="failed",
            error_count=1,
            details=[
                _import_detail(
                    "Geen CSV-bestand gekozen.",
                    field="Bestand",
                    action="Kies eerst een CSV-bestand en klik daarna opnieuw op Uploaden.",
                )
            ],
        )
    return redirect('training')



def upload_wedstrijddata(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        filename = csv_file.name or ""

        if not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Upload een geldig CSV-bestand (.csv).')
            _record_data_import_log(
                request,
                data_type="Wedstrijddata",
                filename=filename,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Bestandstype is ongeldig.",
                        field="Bestand",
                        value=filename,
                        action="Upload een bestand met de extensie .csv.",
                    )
                ],
            )
            return redirect('wedstrijddata')
        upload_selection = _gps_upload_selection(request)
        if not upload_selection:
            _record_data_import_log(
                request,
                data_type="Wedstrijddata",
                filename=filename,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Team, event of spelerslijst is niet geldig.",
                        action="Kies eerst een geldig team en event. Controleer ook of dit team spelers bevat.",
                    )
                ],
            )
            return redirect('wedstrijddata')
        if upload_selection["session_kind"] == "training":
            return upload_file(request)

        try:
            decoded = _decode_uploaded_csv(csv_file)
        except UnicodeDecodeError:
            messages.error(request, 'Het CSV-bestand kon niet worden gelezen. Exporteer het bestand opnieuw als CSV met UTF-8 of Windows-1252 encoding.')
            _record_data_import_log(
                request,
                data_type="Wedstrijddata",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "CSV kon niet worden gelezen.",
                        action="Exporteer het bestand opnieuw als CSV met UTF-8 of Windows-1252 encoding.",
                    )
                ],
            )
            return redirect('wedstrijddata')

        reader = csv.DictReader(decoded, skipinitialspace=True)
        if not reader.fieldnames:
            messages.error(request, 'Het CSV-bestand bevat geen kolomkoppen.')
            _record_data_import_log(
                request,
                data_type="Wedstrijddata",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "CSV bevat geen kolomkoppen.",
                        action="Zorg dat de eerste rij de kolomnamen bevat, zoals Player Last Name en Session Date.",
                    )
                ],
            )
            return redirect('wedstrijddata')
        if not _csv_has_columns(reader, ("Player Last Name", "Session Date")):
            missing_columns = [
                column for column in ("Player Last Name", "Session Date")
                if not _csv_has_columns(reader, (column,))
            ]
            messages.error(request, 'Het CSV-bestand mist verplichte kolommen: Player Last Name en Session Date.')
            _record_data_import_log(
                request,
                data_type="Wedstrijddata",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Verplichte kolom ontbreekt.",
                        field=", ".join(missing_columns) or "Player Last Name / Session Date",
                        action="Voeg deze kolom toe aan de CSV-export en upload het bestand opnieuw.",
                    )
                ],
            )
            return redirect('wedstrijddata')
        if not _csv_has_any_column(reader, ("Total Distance", "HIR (M>20 KM/U)", "Sprints", "HML Distance")):
            messages.error(request, 'Het CSV-bestand bevat geen herkenbare wedstrijd-GPS-kolommen zoals Total Distance, HIR, Sprints of HML Distance.')
            _record_data_import_log(
                request,
                data_type="Wedstrijddata",
                filename=filename,
                upload_selection=upload_selection,
                status="failed",
                error_count=1,
                details=[
                    _import_detail(
                        "Geen herkenbare wedstrijd-GPS-kolommen gevonden.",
                        field="Total Distance / HIR (M>20 KM/U) / Sprints / HML Distance",
                        action="Controleer of de StatsSports-export minimaal een van deze wedstrijdkolommen bevat.",
                    )
                ],
            )
            return redirect('wedstrijddata')

        def first_available_float(row, names):
            normalized = {str(key).strip().lower(): value for key, value in row.items()}
            for name in names:
                raw_value = normalized.get(name.strip().lower())
                if raw_value not in (None, ""):
                    return _csv_float_or_none(raw_value)
            return None

        _ensure_gps_metric_types(GPS_MATCH_METRICS)
        players = upload_selection["players"]
        csv_columns = {str(field or "").strip().lower() for field in (reader.fieldnames or [])}
        seen_sessions = set()
        count = 0
        duplicates = 0
        skipped = 0
        invalid_dates = 0
        unknown_players = 0
        missing_values = 0
        details = []
        source_tag = f"main_upload_match_{upload_selection['event_code']}"

        for row_number, row in enumerate(reader, start=2):
            csv_lastname = _normalize_csv_value(_csv_get(row, 'Player Last Name'))
            if not csv_lastname:
                skipped += 1
                _add_import_issue(
                    details,
                    "Spelernaam ontbreekt.",
                    row=row_number,
                    field="Player Last Name",
                    action="Vul in deze rij de achternaam/spelernaam in zoals die in het gekozen team staat.",
                )
                continue

            player = _find_player_from_gps_lastname(players, csv_lastname, allow_contains=True)
            if not player:
                unknown_players += 1
                _add_import_issue(
                    details,
                    "Speler niet gevonden binnen het gekozen team.",
                    row=row_number,
                    field="Player Last Name",
                    value=csv_lastname,
                    action=f"Controleer de spelling of kies het juiste team. Deze upload staat nu op {upload_selection['team_label']}.",
                )
                continue

            match_date = _parse_statsports_date(_csv_get(row, 'Session Date'))
            if not match_date:
                invalid_dates += 1
                _add_import_issue(
                    details,
                    "Datum ontbreekt of is ongeldig.",
                    row=row_number,
                    field="Session Date",
                    value=_normalize_csv_value(_csv_get(row, 'Session Date')),
                    action="Gebruik een geldige datum, bijvoorbeeld 15/05/2026 of 2026-05-15.",
                )
                continue

            session_key = (player.id, "match", match_date, source_tag)
            if session_key in seen_sessions or _gps_session_exists(player, "match", match_date, source_tag):
                duplicates += 1
                _add_import_issue(
                    details,
                    "Dubbele wedstrijddata gevonden.",
                    row=row_number,
                    value=f"{player.name} op {match_date.strftime('%d-%m-%Y')}",
                    action="Deze speler-datum-event combinatie bestaat al. Verwijder de dubbele rij of kies een ander event als het om een andere wedstrijd/sessie gaat.",
                )
                continue

            week = match_date.isocalendar()[1]
            first_half_load = first_available_float(row, [
                "First Half HML Distance",
                "HML Distance First Half",
                "HML Distance 1st Half",
                "1st Half HML Distance",
                "HML Distance (1st Half)",
                "HML Distance 1H",
                "First Half Load",
                "Load First Half",
                "Load 1st Half",
                "1st Half Load",
                "Eerste helft load",
            ])
            second_half_load = first_available_float(row, [
                "Second Half HML Distance",
                "HML Distance Second Half",
                "HML Distance 2nd Half",
                "2nd Half HML Distance",
                "HML Distance (2nd Half)",
                "HML Distance 2H",
                "Second Half Load",
                "Load Second Half",
                "Load 2nd Half",
                "2nd Half Load",
                "Tweede helft load",
            ])
            metric_columns = {
                'accelerations': ('Accelerations (Absolute)', _csv_int_or_none),
                'decelerations': ('Decelerations (Absolute)', _csv_int_or_none),
                'hsd': ('HIR (M>20 KM/U)', _csv_float_or_none),
                'his': ('HIS (M>25 KM/U)', _csv_float_or_none),
                'total_distance': ('Total Distance', _csv_float_or_none),
                'sprints': ('Sprints', _csv_int_or_none),
                'load': ('HML Distance', _csv_float_or_none),
            }
            valid_metrics = {}
            for code, (column_name, parser) in metric_columns.items():
                if column_name.lower() not in csv_columns:
                    continue
                value = parser(_csv_get(row, column_name))
                if value is None:
                    missing_values += 1
                else:
                    valid_metrics[code] = value
            if first_half_load is not None:
                valid_metrics["first_half_load"] = first_half_load
            if second_half_load is not None:
                valid_metrics["second_half_load"] = second_half_load
            if not valid_metrics:
                skipped += 1
                _add_import_issue(
                    details,
                    "Geen geldige wedstrijdmeetwaarden gevonden.",
                    row=row_number,
                    field="Total Distance / HIR / Sprints / HML Distance",
                    action="Vul minimaal een geldige meetwaarde in of controleer of de kolomnamen uit StatsSports kloppen.",
                )
                continue

            upsert_performance_session_metrics(
                player=player,
                session_kind='match',
                session_date=match_date,
                week=week,
                metrics=valid_metrics,
                source_tag=source_tag,
                match_source=True,
            )
            seen_sessions.add(session_key)
            count += 1

        _show_gps_import_feedback(
            request,
            imported=count,
            duplicates=duplicates,
            skipped=skipped,
            invalid_dates=invalid_dates,
            unknown_players=unknown_players,
            missing_values=missing_values,
            label=f"{upload_selection['team_label']} {upload_selection['event_label'].lower()}",
        )
        error_count = skipped + invalid_dates + unknown_players + missing_values
        _record_data_import_log(
            request,
            data_type="Wedstrijddata",
            filename=filename,
            upload_selection=upload_selection,
            status=_import_log_status(processed_count=count, duplicate_count=duplicates, error_count=error_count),
            processed_count=count,
            duplicate_count=duplicates,
            error_count=error_count,
            details=details,
        )
        return redirect('wedstrijddata')

    if request.method == 'POST':
        messages.error(request, 'Kies eerst een CSV-bestand om te uploaden.')
        _record_data_import_log(
            request,
            data_type="Wedstrijddata",
            status="failed",
            error_count=1,
            details=[
                _import_detail(
                    "Geen CSV-bestand gekozen.",
                    field="Bestand",
                    action="Kies eerst een CSV-bestand en klik daarna opnieuw op Uploaden.",
                )
            ],
        )
    return redirect('wedstrijddata')


def beweeganalyse(request):
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")

    player_param = (
        request.POST.get("player_id")
        or request.GET.get("player_id")
        or request.GET.get("playerid")
    )
    date_param = (
        request.POST.get("analysis_date")
        or request.GET.get("analysis_date")
        or request.GET.get("datum")
    )

    selected_date = parse_date(date_param) if date_param else timezone.localdate()
    if selected_date is None:
        selected_date = timezone.localdate()

    selected_player = None
    if player_param:
        selected_player = Player.objects.filter(id=player_param).first()
    if selected_player is None:
        selected_player = players.first()

    punten = list(
        BeweeganalysePunt.objects.filter(is_active=True, onderdeel__is_active=True)
        .select_related("onderdeel")
        .prefetch_related("oefeningen")
        .order_by("onderdeel__sort_order", "sort_order", "id")
    )

    if request.method == "POST" and selected_player:
        sessie, _ = BeweeganalyseSessie.objects.get_or_create(
            player=selected_player,
            date=selected_date,
        )
        action = (request.POST.get("action") or "").strip().lower()

        if action == "upload_video":
            uploaded_file = request.FILES.get("video_file")
            if not uploaded_file:
                messages.error(request, "Kies eerst een videobestand om te uploaden.")
            else:
                ffmpeg_bin = shutil.which("ffmpeg")
                if not ffmpeg_bin:
                    messages.error(
                        request,
                        "FFmpeg is niet gevonden op de server. Installatie van FFmpeg is nodig voor auto-compilatie (normaal + 0.5x).",
                    )
                else:
                    ext = os.path.splitext(uploaded_file.name or "")[1].lower() or ".mp4"
                    token = uuid.uuid4().hex[:10]
                    tmp_rel = f"beweeganalyse_videos/tmp_{selected_player.id}_{selected_date.isoformat()}_{token}{ext}"
                    tmp_rel = tmp_rel.replace(":", "-")
                    tmp_abs = default_storage.path(tmp_rel)
                    os.makedirs(os.path.dirname(tmp_abs), exist_ok=True)

                    compiled_rel = f"beweeganalyse_videos/compiled_{selected_player.id}_{selected_date.isoformat()}_{token}.mp4"
                    compiled_rel = compiled_rel.replace(":", "-")
                    compiled_abs = default_storage.path(compiled_rel)
                    os.makedirs(os.path.dirname(compiled_abs), exist_ok=True)

                    tmp_saved = default_storage.save(tmp_rel, uploaded_file)
                    tmp_abs = default_storage.path(tmp_saved)

                    cmd = [
                        ffmpeg_bin,
                        "-y",
                        "-i",
                        tmp_abs,
                        "-filter_complex",
                        "[0:v]setpts=PTS-STARTPTS[v1];[0:v]setpts=2*(PTS-STARTPTS)[v2];[v1][v2]concat=n=2:v=1:a=0[v]",
                        "-map",
                        "[v]",
                        "-an",
                        "-c:v",
                        "libx264",
                        "-preset",
                        "veryfast",
                        "-crf",
                        "23",
                        "-pix_fmt",
                        "yuv420p",
                        compiled_abs,
                    ]

                    try:
                        proc = subprocess.run(cmd, capture_output=True, text=True)
                        if proc.returncode != 0 or (not os.path.exists(compiled_abs)):
                            msg = (proc.stderr or proc.stdout or "").strip()
                            short_msg = msg.splitlines()[-1] if msg else "Onbekende fout."
                            messages.error(request, f"Compilatie maken is mislukt: {short_msg}")
                        else:
                            if sessie.video_file:
                                sessie.video_file.delete(save=False)
                            sessie.video_file.name = compiled_rel
                            sessie.save(update_fields=["video_file", "updated_at"])
                            messages.success(request, "Succesvol opgeslagen. Video geüpload en compilatie (normaal + 0.5x) aangemaakt.")
                    finally:
                        if default_storage.exists(tmp_saved):
                            default_storage.delete(tmp_saved)
            return redirect(
                f"{reverse('beweeganalyse')}?player_id={selected_player.id}&analysis_date={selected_date.isoformat()}"
            )

        if action == "delete_video":
            if sessie.video_file:
                sessie.video_file.delete(save=False)
                sessie.video_file = None
                sessie.save(update_fields=["video_file", "updated_at"])
                messages.success(request, "Video verwijderd.")
            else:
                messages.warning(request, "Er stond geen video om te verwijderen.")
            return redirect(
                f"{reverse('beweeganalyse')}?player_id={selected_player.id}&analysis_date={selected_date.isoformat()}"
            )

        for punt in punten:
            score_raw = (request.POST.get(f"score_{punt.id}") or "").strip()
            comment_val = (request.POST.get(f"comment_{punt.id}") or "").strip()
            priority_flag = request.POST.get(f"priority_{punt.id}") == "1"

            score_val = None
            if score_raw:
                try:
                    parsed_score = int(score_raw)
                    if 1 <= parsed_score <= 4:
                        score_val = parsed_score
                except (TypeError, ValueError):
                    score_val = None

            BeweeganalyseBeoordeling.objects.update_or_create(
                sessie=sessie,
                punt=punt,
                defaults={
                    "score": score_val,
                    "priority_flag": priority_flag,
                    "comment": comment_val,
                },
            )

        messages.success(request, "Beoordeling opgeslagen.")
        return redirect(
            f"{reverse('beweeganalyse')}?player_id={selected_player.id}&analysis_date={selected_date.isoformat()}"
        )

    existing_scores = {}
    sessie = None
    if selected_player:
        sessie = (
            BeweeganalyseSessie.objects.filter(player=selected_player, date=selected_date)
            .prefetch_related("beoordelingen")
            .first()
        )
        if sessie:
            existing_scores = {b.punt_id: b for b in sessie.beoordelingen.all()}

    sections = []
    current_onderdeel_id = None
    current_section = None
    for punt in punten:
        if current_onderdeel_id != punt.onderdeel_id:
            current_onderdeel_id = punt.onderdeel_id
            current_section = {
                "onderdeel": punt.onderdeel,
                "rows": [],
            }
            sections.append(current_section)
        current_section["rows"].append(
            {
                "punt": punt,
                "existing": existing_scores.get(punt.id),
                "exercise_suggestions": [
                    oef.name for oef in punt.oefeningen.all() if oef.is_active
                ],
            }
        )

    context = {
        "players": players,
        "selected_player": selected_player,
        "selected_date": selected_date,
        "selected_sessie": sessie,
        "sections": sections,
    }
    return render(request, "beweeganalyse.html", context)



