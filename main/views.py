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
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django import forms
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
    PlayerMonitoringProfile,
)
from .performance_3nf import fetch_performance_rows, mean, upsert_performance_session_metrics


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
        fields = ["date", "activities", "notes"]


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

    # ---------- BASIS ----------
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")
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
    week_start_date = today - timedelta(days=today.weekday())
    week_end_date = week_start_date + timedelta(days=6)
    current_week_dayprograms = (
        DayProgramEntry.objects.filter(date__gte=week_start_date, date__lte=week_end_date)
        .order_by("date")
    )

    # ---------- CONTEXT ----------
    context = {
        "title": "Willem II Dashboard",
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
        "current_week_start": week_start_date,
        "current_week_end": week_end_date,
    }

    return render(request, "Load_dashboard.html", context)




# ---------- WEEKPROGRAMMA BEWERKEN ----------
def edit_weekday(request, pk):
    day = get_object_or_404(DayProgramEntry, pk=pk)

    if request.method == "POST":
        form = WeekProgramForm(request.POST, instance=day)
        if form.is_valid():
            form.save()
            messages.success(request, "Trainingsdag succesvol gewijzigd.")
            return redirect("dashboard")

    return redirect("dashboard")


# ---------- WEEKPROGRAMMA VERWIJDEREN ----------
def delete_weekday(request, pk):
    day = get_object_or_404(DayProgramEntry, pk=pk)
    day.delete()
    messages.success(request, "Trainingsdag succesvol verwijderd.")
    return redirect("dashboard")


# ---------- WEEKPROGRAMMA TOEVOEGEN ----------
def add_weekday(request):
    if request.method == "POST":
        form = WeekProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trainingsdag succesvol toegevoegd.")
            return redirect("dashboard")

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

            session = NutritionIntakeSession.objects.create(
                player=p,
                date=parsed_date,
                goal=request.POST.get("goal", "").strip(),
                next_meeting_goal=request.POST.get("next_meeting_goal", "").strip(),
            )
            meal_values = {
                "breakfast": request.POST.get("breakfast", "").strip(),
                "snack1": request.POST.get("snack1", "").strip(),
                "lunch": request.POST.get("lunch", "").strip(),
                "snack2": request.POST.get("snack2", "").strip(),
                "dinner": request.POST.get("dinner", "").strip(),
                "snack3": request.POST.get("snack3", "").strip(),
                "supplements": request.POST.get("supplements", "").strip(),
            }
            for meal_key, value in meal_values.items():
                NutritionIntakeItem.objects.create(
                    session=session,
                    meal_key=meal_key,
                    value=value,
                )

            # Optioneel: nutrition_focus op Player model
            if "nutrition_focus" in request.POST:
                profile = _get_or_create_monitoring_profile(p)
                profile.nutrition_focus = request.POST.get("nutrition_focus", "").strip()
                profile.save(update_fields=["nutrition_focus", "updated_at"])

            messages.success(request, f"Intake voor {p.name} is opgeslagen.")
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
    selected_metric_field = metric_field_map[selected_metric]

    players = Player.objects.select_related("monitoring_profile").all().order_by("name")
    week_targets, _ = TrainingWeekTarget.objects.get_or_create(
        name="Geplande weektargets training"
    )

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
        messages.success(request, "Geplande weektargets opgeslagen!")
        return redirect("training")

    week_target_rows = [
        {
            "field_name": field_name,
            "label": label,
            "values": parse_weektarget_value(getattr(week_targets, field_name, "")),
        }
        for field_name, label in day_field_map
    ]
    rows = fetch_performance_rows("training")

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
    selected_player = Player.objects.filter(name=selected_player_name).first() if selected_player_name else None
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

    POSITION_TARGETS = {
        "Spits": {"km": 11.5, "hir": 950, "his": 200, "a_d": 180},
        "Targetman": {"km": 11, "hir": 500, "his": 75, "a_d": 160},
        "Buitenspeler": {"km": 11, "hir": 1000, "his": 150, "a_d": 150},
        "Dynamische middenvelder": {"km": 12, "hir": 950, "his": 200, "a_d": 180},
        "Controlerende middenvelder": {"km": 12, "hir": 700, "his": 150, "a_d": 180},
        "Centrale verdediger": {"km": 10.5, "hir": 500, "his": 100, "a_d": 160},
        "Vleugelverdediger": {"km": 11, "hir": 1000, "his": 250, "a_d": 190},
    }

    players = Player.objects.select_related("monitoring_profile").all().order_by("name")
    selected_player_name = request.GET.get("player")
    selected_player = Player.objects.filter(name=selected_player_name).first() if selected_player_name else None

    all_rows = fetch_performance_rows("match")
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

        "active_page": "wedstrijd",
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

    players = Player.objects.select_related("monitoring_profile").all().order_by("name")
    test_rows = fetch_performance_rows("test")

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
        for row in test_rows
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
    for row in test_rows:
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
        for row in test_rows:
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

    player_id = request.GET.get("player_id")
    tab_param = (request.GET.get("tab") or "").strip().lower()
    if tab_param not in {"invoer", "profiel"}:
        tab_param = "profiel" if player_id else "invoer"
    selected_player = None
    percentiles = {}

    if player_id:
        selected_player = get_object_or_404(Player.objects.select_related("monitoring_profile"), id=player_id)
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
        player_obj = get_object_or_404(Player, id=request.POST.get("player_id"))
        test_date = request.POST.get("test_date")
        if not test_date:
            return redirect("/testdata/?tab=invoer")

        parsed_date = datetime.strptime(test_date, "%Y-%m-%d").date()
        upsert_performance_session_metrics(
            player=player_obj,
            session_kind="test",
            session_date=parsed_date,
            metrics={
                "sprint_10": request.POST.get("sprint_10"),
                "sprint_30": request.POST.get("sprint_30"),
                "cmj": request.POST.get("cmj"),
                "isrt": request.POST.get("isrt"),
                "submax": request.POST.get("submax"),
                "curr_weight": request.POST.get("curr_weight"),
                "length": request.POST.get("length"),
                "sum_skinfolds": request.POST.get("sum_skinfolds"),
            },
            source_tag="main_manual_test",
        )
        return redirect("/testdata/?tab=invoer")

    context = {
        "players": players,
        "selected_player": selected_player,
        "test_data": test_data,
        "team_avg": team_avg,
        "percentiles": percentiles,
        "active_testdata_tab": tab_param,
        "team_profile_rows": team_profile_rows,
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
    injuries = InjuryCase.objects.select_related(
        "player", "injury_type_ref", "phase_ref", "status_ref"
    ).order_by("started_on")
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")

    selected_player_id = request.GET.get("player_id")
    selected_player_name = request.GET.get("player")
    selected_player = None

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
                return redirect("revalidatie")

            try:
                player = Player.objects.get(id=player_id)
            except Player.DoesNotExist:
                messages.error(request, "Ongeldige speler geselecteerd.")
                return redirect("revalidatie")

            _upsert_injury_case(
                player=player,
                injury_type=injury_type,
                start_date_value=start_date,
                duration_value=None,
                expected_return_value=expected_return,
                phase=phase,
            )
            messages.success(request, f"Blessure voor {player.name} toegevoegd.")
            return redirect("revalidatie")

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
            return redirect(f"/revalidatie/?player_id={player_id}")
        if selected_player:
            return redirect(f"/revalidatie/?player_id={selected_player.id}")
        return redirect("revalidatie")

    context = {
        "injuries": [_injury_to_ui(injury) for injury in injuries],
        "players": players,
        "selected_player": selected_player,
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
    AttendanceRecord,
    AttendanceStatus,
    IndividualDayPlan,
    IndividualDayPlanNote,
    IndividualDayPlanNoteType,
    Player,
    Programma,
    ProgrammaOefening,
    RPEEntry,
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

    players = Player.objects.select_related("monitoring_profile").all().order_by("name")

    # Haal geselecteerde speler uit URL parameters
    player_id = request.GET.get("player_id")
    selected_player = None
    programma = None
    oefeningen = []
    day_program = None
    video_previews = []

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
        selected_player = get_object_or_404(Player.objects.select_related("monitoring_profile"), id=player_id)

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
        day_program = SimpleNamespace(
            date=plan.date,
            program_text=note.content,
            opmerkingen=remarks_note.content,
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
            return redirect(f"/individuele_programmas/?player_id={player_id}")

    context = {
        "players": players,
        "selected_player": selected_player,
        "day_program": day_program,
        "programma": programma,
        "oefeningen": oefeningen,
        "video_previews": video_previews,
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

def rpe_view(request):
    """RPE dashboard met robuuste POST-afhandeling en 3NF velden."""

    players = Player.objects.select_related("monitoring_profile").all().order_by("name")
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

    # 1ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ Datum ophalen & converteren naar date-object
    selected_date = request.GET.get("date")

    if selected_date:
        # GET levert een string -> converteren naar date
        date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        date = timezone.now().date()

    # 2ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ Spelers ophalen
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")

    # 3ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ Entries van deze datum ophalen
    existing_entries = WellnessEntry.objects.filter(date=date)

    filled_player_ids = set(existing_entries.values_list("player_id", flat=True))

    # 4ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ Verdeling in ingevuld / niet ingevuld
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
        date_post = request.POST.get("date")

        # Datum van POST opnieuw correct converteren
        date_obj = datetime.strptime(date_post, "%Y-%m-%d").date()

        player = Player.objects.get(id=player_id)

        WellnessEntry.objects.update_or_create(
            player=player,
            date=date_obj,
            defaults={
                "sleep": sleep,
                "mood": mood,
                "fitness": fitness,
                "soreness": soreness,
                "comment": comment
            }
        )

        # Refresh pagina zodat speler naar 'wel ingevuld' gaat
        return redirect(f"/wellness/?date={date_obj}")

    # 6ÃƒÂ¯Ã‚Â¸Ã‚ÂÃƒÂ¢Ã†â€™Ã‚Â£ Context + render
    return render(request, "wellness.html", {
    "date": date.strftime("%Y-%m-%d"),
    "players_filled": players_filled,
    "players_not_filled": players_not_filled,
    "existing_entries": existing_entries,
})



# =====================================
#   HIT PAGINA VIEW
# =====================================

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Player, PlayerSpeedTest, HitAsrPlanSession, HitAsrPlanEntry


def hit_page(request):
    """HIT pagina: calculator + individualiserings-tools."""
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
        return redirect("/hit/")

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
            return redirect("/hit/")

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
            return redirect("/hit/")

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
        return redirect("/hit/")

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

    # 2. Spelers ophalen
    players = Player.objects.select_related("monitoring_profile").all().order_by("name")

    status_qs = AttendanceStatus.objects.filter(is_active=True).order_by("sort_order", "label")
    status_choices = [(status.code, status.label) for status in status_qs]
    default_status = status_qs.filter(code="overig").first() or status_qs.first()

    # 3. Voor elke speler een AttendanceRecord entry ophalen of automatisch aanmaken
    records = []
    for player in players:
        aanwezigheid, created = AttendanceRecord.objects.get_or_create(
            player=player,
            date=chosen_date,
            defaults={"status": default_status, "completed": False},
        )
        records.append(
            SimpleNamespace(
                id=aanwezigheid.id,
                player=aanwezigheid.player,
                status=aanwezigheid.status.code if aanwezigheid.status else "overig",
                completed=aanwezigheid.completed,
                date=aanwezigheid.date,
            )
        )

    # 4. Navigatie (vorige dag / volgende dag)
    previous_day = chosen_date - timedelta(days=1)
    next_day = chosen_date + timedelta(days=1)

    context = {
        "players": players,
        "records": records,
        "chosen_date": chosen_date,
        "previous_day": previous_day,
        "next_day": next_day,
        "status_choices": status_choices,
    }

    return render(request, "aanwezigheden.html", context)


# -------------------------------------
# AANWEZIGHEDEN UPDATE
# -------------------------------------
def aanwezigheden_update(request, record_id):
    """Update ÃƒÆ’Ã‚Â©ÃƒÆ’Ã‚Â©n aanwezigheidsrecord (dropdown + checkmark)."""

    aanwezigheid = get_object_or_404(AttendanceRecord, id=record_id)

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

    return redirect(f"/aanwezigheden/?date={aanwezigheid.date}")


def overig(request):
    page = request.GET.get('page', 'menu')

    staff_members = Staff.objects.all().order_by('name')
    players = Player.objects.all().order_by('name')

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
        return render(request, 'overig.html', {
            'page': 'pop',
            'players': players,
            'staff': staff_members,
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
    # JEUGD WILLEM II
    # ======================================
    if page == "jeugd":
        if request.method == "POST":
            section = request.POST.get("section")
            text = request.POST.get("text", "")
            if section:
                OverigNote.objects.create(
                    note_type="section",
                    page_key="jeugd",
                    section_key=section,
                    text=text.strip(),
                )
            return redirect("/overig/?page=jeugd")

        return render(request, 'overig.html', {
            'page': 'jeugd',
            'players': players,
            'staff': staff_members,
            "jeugd_texts": {
                "leerlijn": section_text("jeugd", "leerlijn"),
                "individueel": section_text("jeugd", "individueel"),
                "processen": section_text("jeugd", "processen"),
                "toekomst": section_text("jeugd", "toekomst"),
            },
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

    if page in {"fysiek-wetenschap", "ontwikkelingsgesprekken", "vakantieprogramma"}:
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
        return redirect(f"/beleid/?tab={beleid_tab}&subtab={beleid_subtab}")

    return render(request, "beleid.html", {
        "beleid_tab": beleid_tab,
        "beleid_subtab": beleid_subtab,
        "beleid_current_text": section_text(section_key),
        "beleid_images": section_images(section_key),
    })


@login_required
def staf(request):
    staff_members = Staff.objects.select_related("role_ref").all().order_by("name")

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        role_name = (request.POST.get("role_name") or "").strip()
        image = request.FILES.get("image")

        if name and role_name:
            role_obj, _ = StaffRole.objects.get_or_create(name=role_name)
            Staff.objects.create(
                name=name,
                role_ref=role_obj,
                image=image if image else None,
            )
            return redirect("staf")

    return render(request, "staf.html", {
        "staff_members": staff_members,
    })


def player_data(request, player_id):
    """
    Geeft JSON terug met de voortgang van gewicht en huidplooien
    voor ??n specifieke speler. Wordt aangeroepen als je op een speler klikt.
    """
    from .models import Player

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


def upload_file(request):
    """Uploadt een StatsSports CSV en schrijft trainingdata naar 3NF performance-tabellen."""
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Upload een geldig CSV-bestand (.csv).')
            return redirect('training')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        def safe_float(value):
            try:
                return float(value)
            except Exception:
                return 0.0

        def safe_int(value):
            try:
                return int(float(value))
            except Exception:
                return 0

        count = 0

        for row in reader:
            try:
                csv_lastname = (row.get('Player Last Name') or '').replace('"', '').strip().lower()
                if not csv_lastname:
                    continue

                player = None
                for p in Player.objects.all():
                    db_lastname = p.name.lower().strip().split()[-1]
                    if db_lastname == csv_lastname:
                        player = p
                        break

                if not player:
                    continue

                date_raw = (row.get('Session Date') or '').replace('"', '').strip()
                try:
                    date_obj = datetime.strptime(date_raw, '%d/%m/%Y').date()
                except Exception:
                    continue

                week = date_obj.isocalendar()[1]
                upsert_performance_session_metrics(
                    player=player,
                    session_kind='training',
                    session_date=date_obj,
                    week=week,
                    metrics={
                        'total_distance': safe_float(row.get('Total Distance')),
                        'hsd': safe_float(row.get('HIR (M>20 KM/U)')),
                        'sprints': safe_int(row.get('Sprints')),
                        'load': 0,
                    },
                    source_tag='main_upload_training',
                )
                count += 1
            except Exception:
                continue

        messages.success(request, f'{count} trainingsregels succesvol geimporteerd in 3NF.')
        return redirect('training')

    return redirect('training')



def upload_wedstrijddata(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Upload een geldig CSV-bestand (.csv).')
            return redirect('training')

        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded, skipinitialspace=True)

        def safe_float(v):
            try:
                return float(v)
            except Exception:
                return 0.0

        def safe_int(v):
            try:
                return int(float(v))
            except Exception:
                return 0

        count = 0

        for row in reader:
            try:
                csv_lastname = (row.get('Player Last Name') or '').strip().lower()
                if not csv_lastname:
                    continue

                csv_lastname = csv_lastname.replace('Ã„Â', 'c').replace('Ã„â€¡', 'c').replace('Ã…Â¡', 's')

                player = None
                for p in Player.objects.all():
                    name_clean = p.name.lower().replace('Ã„Â', 'c').replace('Ã„â€¡', 'c').replace('Ã…Â¡', 's')
                    if csv_lastname in name_clean:
                        player = p
                        break

                if not player:
                    continue

                raw_date = (row.get('Session Date') or '').strip()
                try:
                    match_date = datetime.strptime(raw_date, '%d/%m/%Y').date()
                except Exception:
                    continue

                week = match_date.isocalendar()[1]
                upsert_performance_session_metrics(
                    player=player,
                    session_kind='match',
                    session_date=match_date,
                    week=week,
                    metrics={
                        'accelerations': safe_int(row.get('Accelerations (Absolute)')),
                        'decelerations': safe_int(row.get('Decelerations (Absolute)')),
                        'hsd': safe_float(row.get('HIR (M>20 KM/U)')),
                        'his': safe_float(row.get('HIS (M>25 KM/U)')),
                        'total_distance': safe_float(row.get('Total Distance')),
                        'sprints': safe_int(row.get('Sprints')),
                        'load': safe_float(row.get('HML Distance')),
                    },
                    source_tag='main_upload_match',
                )
                count += 1
            except Exception:
                continue

        messages.success(request, f'{count} wedstrijdregels succesvol geimporteerd in 3NF.')
        return redirect('training')

    return redirect('training')


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
                            messages.success(request, "Video geupload en compilatie (normaal + 0.5x) aangemaakt.")
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



