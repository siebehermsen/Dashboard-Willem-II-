from django.http import HttpResponse
import csv
from .models import Player, Injury, TrainingData, DayProgram, PlayerTest, Oefening
from django.db.models import Avg, Sum
from django.http import JsonResponse
from .models import Player, WellnessEntry
from django.utils import timezone
from .models import Player, Aanwezigheid
from django.shortcuts import render, redirect
from .models import Overig
from .models import Player, Overig, Staff
from .models import WedstrijdData, Player
from django.db.models import Avg, Min, Max
from django.utils import timezone
from .models import Match

# ---------- IMPORTS ----------
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Avg
from django import forms
from datetime import datetime, timedelta
from django.conf import settings



# ---------- INLINE FORM (GEEN forms.py NODIG) ----------
class WeekProgramForm(forms.ModelForm):
    class Meta:
        model = DayProgram
        fields = ["date", "activities", "notes"]


# ---------- HOME / TEST ----------
def home(request):
    return HttpResponse("✅ Django werkt correct!")


# ---------- DASHBOARD ----------
def dashboard(request):

    # ---------- BASIS ----------
    players = Player.objects.all().order_by("name")
    dayprograms = DayProgram.objects.all().order_by("date")
    weekform = WeekProgramForm()

    # ---------- CLUBLOGO’S ----------
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
        "Vitesse": "https://upload.wikimedia.org/wikipedia/en/c/c8/SBV_Vitesse_logo.svg/987px-ADO_Den_Haag_logo.svg.png",
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

        # ✅ SEIZOENSPLANNING IMPORTEREN (harde reset)
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

                Match.objects.create(
                    kickoff=kickoff,
                    home=m["home"],
                    away=m["away"],
                )
                created_count += 1

            messages.success(
                request,
                f"Seizoensplanning geïmporteerd. Nieuw: {created_count}, geüpdatet: {updated_count}, verwijderd: alles opnieuw opgebouwd.",
            )
            return redirect("dashboard")

        # ✅ Weekplanning opslaan
        if request.POST.get("form_type") == "add_weekday":
            weekform = WeekProgramForm(request.POST)
            if weekform.is_valid():
                weekform.save()
                messages.success(request, "Weekplanning succesvol toegevoegd.")
                return redirect("dashboard")

    # ---------- REVALIDATIES ----------
    rehab_players = Injury.objects.all().order_by("-start_date")

    # ---------- GEMIDDELDE VETPERCENTAGE ----------
    avg_fat = None

    # ---------- KOMENDE WEDSTRIJD (UIT DATABASE) ----------
    now = timezone.now()
    upcoming_match = Match.objects.filter(kickoff__gte=now).order_by("kickoff").first()

    home_logo = logos.get(upcoming_match.home, "") if upcoming_match else ""
    away_logo = logos.get(upcoming_match.away, "") if upcoming_match else ""

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
    }

    return render(request, "Load_dashboard.html", context)




# ---------- WEEKPROGRAMMA BEWERKEN ----------
def edit_weekday(request, pk):
    day = get_object_or_404(DayProgram, pk=pk)

    if request.method == "POST":
        form = WeekProgramForm(request.POST, instance=day)
        if form.is_valid():
            form.save()
            messages.success(request, "Trainingsdag succesvol gewijzigd.")
            return redirect("dashboard")

    return redirect("dashboard")


# ---------- WEEKPROGRAMMA VERWIJDEREN ----------
def delete_weekday(request, pk):
    day = get_object_or_404(DayProgram, pk=pk)
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

        # Blessure opslaan
        Injury.objects.create(
            name=name,
            injury_type=injury_type,
            start_date=start_date,
            duration=duration,
            phase=phase,
        )

        messages.success(request, f"Blessure van {name} succesvol toegevoegd.")

    # Altijd terug naar dashboard
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


# ---------- BLESSURE TOEVOEGEN ----------
def add_rehab(request):
    if request.method == "POST":
        Injury.objects.create(
            name=request.POST.get("name"),
            injury_type=request.POST.get("injury_type"),
            start_date=request.POST.get("start_date"),
            duration=request.POST.get("duration"),
            phase=request.POST.get("phase"),
        )
    return redirect("dashboard")



from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Player, NutritionDay


def nutrition_view(request):
    """
    Voedingsdashboard:
    - Weekvoedingsplanning
    - Spelerselectie + aandachtspunt
    """

    days = [
        "Maandag", "Dinsdag", "Woensdag",
        "Donderdag", "Vrijdag", "Zaterdag", "Zondag"
    ]
    current_day = days[datetime.now().weekday()]

    players = Player.objects.all().order_by("name")
    selected_player = None

    player_id = request.GET.get("player_id")
    if player_id:
        selected_player = get_object_or_404(Player, id=player_id)

    # ======================
    # POST
    # ======================
    if request.method == "POST":

        # Speler-aandachtspunt
        if "nutrition_focus" in request.POST:
            player_id = request.POST.get("player_id")
            selected_player = get_object_or_404(Player, id=player_id)

            selected_player.nutrition_focus = request.POST.get("nutrition_focus")
            selected_player.save()

            messages.success(
                request,
                f"Aandachtspunt voor {selected_player.name} is opgeslagen."
            )
            return redirect(f"/nutrition/?player_id={player_id}")

        # Weekvoedingsschema
        if "nutrition_day" in request.POST:
            for day in days:
                meal = request.POST.get(f"meal_{day}")
                color = request.POST.get(f"color_{day}")

                if meal:
                    NutritionDay.objects.update_or_create(
                        day=day,
                        defaults={
                            "meal": meal,
                            "color": color or "green",
                        }
                    )

            messages.success(request, "Weekvoedingsschema is opgeslagen.")
            return redirect("/nutrition/")

    nutrition_days = {
        day: NutritionDay.objects.filter(day=day).first()
        for day in days
    }

    context = {
        "active_page": "nutrition",
        "days": days,
        "current_day": current_day,
        "players": players,
        "selected_player": selected_player,
        "nutrition_days": nutrition_days,
    }

    return render(request, "nutrition.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify

from .models import Antropometry



from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.text import slugify
from .models import Player, Antropometry

def skinfold_view(request):
    """
    Antropometrische metingen:
    - Skinfolds
    - Girths
    - Algemene gegevens
    - Berekende vetpercentages (JS → hidden inputs)
    """

    # ======================
    # BASIS DATA
    # ======================
    players = Player.objects.all().order_by("name")

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

    # ======================
    # POST → OPSLAAN
    # ======================
    if request.method == "POST":

        player_id = request.POST.get("player_id")
        measurement_date = request.POST.get("measurement_date")

        if not player_id or not measurement_date:
            messages.error(request, "Speler en datum zijn verplicht.")
            return redirect("/nutrition/huidplooien/")

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

        Antropometry.objects.update_or_create(
            player=player,
            date=measurement_date,
            defaults=data,
        )

        messages.success(
            request,
            f"Antropometrische metingen voor {player.name} zijn opgeslagen."
        )

        return redirect(f"/nutrition/huidplooien/?player={player.id}")

    # ======================
    # GET → DATA LADEN
    # ======================
    selected_player = None
    antropometry = None

    skinfold_rows = []
    girth_values = {}
    fat_values = {}

    player_id = request.GET.get("player")

    if player_id:
        selected_player = Player.objects.filter(id=player_id).first()

        if selected_player:
            antropometry = (
                Antropometry.objects
                .filter(player=selected_player)
                .order_by("-date")
                .first()
            )

            if antropometry:
                # ---- Skinfold rows (⬅️ MINI AANPASSING)
                for site in skinfold_sites:
                    field = skinfold_field_map[site]

                    skinfold_rows.append({
                        "site": site,
                        "key": slugify(site),
                        "m1": getattr(antropometry, f"{field}_m1"),
                        "m2": getattr(antropometry, f"{field}_m2"),
                        "m3": getattr(antropometry, f"{field}_m3"),
                    })

                # ---- Girths
                for site, field in girth_field_map.items():
                    key = slugify(site)
                    girth_values[key] = {
                        "m1": getattr(antropometry, f"{field}_m1"),
                        "m2": getattr(antropometry, f"{field}_m2"),
                        "m3": getattr(antropometry, f"{field}_m3"),
                    }

                # ---- Vetpercentages
                fat_values = {
                    "dw": antropometry.fat_dw,
                    "faulkner": antropometry.fat_faulkner,
                    "carter": antropometry.fat_carter,
                    "average": antropometry.fat_average,
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

        # ⬇️ BELANGRIJK
        "skinfold_rows": skinfold_rows,
        "girth_values": girth_values,
        "fat_values": fat_values,
    }

    return render(request, "nutrition.html", context)







from django.db.models import Avg

from django.db.models import Avg

from django.db.models import Avg, Sum

def training(request):
    """
    Pagina voor trainingsanalyse — toont vergelijking tussen spelers (load, afstand, sprints)
    én een individuele trendgrafiek per speler.
    """
    import json
    import math
    from django.db.models import Sum, Avg
    from .models import TrainingData, Player

    # 📋 Metric selectie (default = load)
    selected_metric = request.GET.get("metric", "load")

    # 📋 Alle spelers
    players = Player.objects.all().order_by("name")

    # 📊 Samenvatting per speler
    player_summary = (
        TrainingData.objects.values("player__name")
        .annotate(
            total_distance=Sum("total_distance"),
            total_sprints=Sum("sprints"),
            total_load=Sum("load"),
            avg_load=Avg("load"),
        )
        .order_by("-total_load")
    )

    # 📈 Data voor groepsgrafiek
    chart_labels = [p["player__name"] for p in player_summary]
    chart_loads = [float(p["total_load"] or 0) for p in player_summary]
    chart_distances = [float(p["total_distance"] or 0) for p in player_summary]
    chart_sprints = [float(p["total_sprints"] or 0) for p in player_summary]

    # 📉 Gemiddelden
    avg_load = sum(chart_loads) / len(chart_loads) if chart_loads else 0
    avg_distance = sum(chart_distances) / len(chart_distances) if chart_distances else 0
    avg_sprints = sum(chart_sprints) / len(chart_sprints) if chart_sprints else 0

    # 📋 Alle ruwe training data (voor tabel 1)
    all_training_data = (
        TrainingData.objects.values(
            "week", "player__name", "total_distance", "hsd", "sprints", "load"
        ).order_by("week", "player__name")
    )

    # 🧍‍♂️ Individuele spelertrend
    selected_player_name = request.GET.get("player")
    selected_player = None
    trend_labels, trend_loads, trend_sprints = [], [], []

    if selected_player_name:
        selected_player = Player.objects.filter(name=selected_player_name).first()
        if selected_player:
            trend_data = (
                TrainingData.objects.filter(player=selected_player)
                .values("week")
                .annotate(
                    avg_load=Avg("load"),
                    avg_sprints=Avg("sprints"),
                )
                .order_by("week")
            )
            trend_labels = [f"Wk {d['week']}" for d in trend_data]
            trend_loads = [float(d["avg_load"] or 0) for d in trend_data]
            trend_sprints = [float(d["avg_sprints"] or 0) for d in trend_data]

    # -------------------------------------------------------------
    # ⭐ EWMA BEREKENING
    # -------------------------------------------------------------
    def compute_ewma(values, lambda_val):
        result_list = []
        for i in range(len(values)):
            total = 0
            for j in range(i + 1):
                days_since = i - j
                weight = math.pow(1 - lambda_val, days_since)
                val = values[j] if values[j] is not None else 0
                total += weight * val * lambda_val
            result_list.append(total)
        return result_list

    lambda_acute = 2 / 8     # EWMA-7
    lambda_chronic = 2 / 29  # EWMA-28

    # 📌 Dynamische metric: load, total_distance, hsd, sprints, etc.
    weekly_data = (
        TrainingData.objects.values("week")
        .annotate(value=Avg(selected_metric))
        .order_by("week")
    )

    weeks = [d["week"] for d in weekly_data]
    metric_values = [float(d["value"] or 0) for d in weekly_data]

    acute_values = compute_ewma(metric_values, lambda_acute)
    chronic_values = compute_ewma(metric_values, lambda_chronic)

    # -------------------------------------------------------------
    # ⭐ NIEUW: TRAININGDATA PER WEEK (voor jouw tabel)
    # -------------------------------------------------------------
    training_data = (
        TrainingData.objects.values("week")
        .annotate(
            total_distance=Sum("total_distance"),
            hsd=Sum("hsd"),
            sprints=Sum("sprints"),
            load=Sum("load"),
        )
        .order_by("week")
    )

    # ACWR (simple ratio week / vorige week)
    training_data = list(training_data)
    for i in range(len(training_data)):
        if i == 0:
            training_data[i]["acwr"] = None
        else:
            prev = training_data[i - 1]["load"] or 1
            training_data[i]["acwr"] = round(training_data[i]["load"] / prev, 2)

    # -------------------------------------------------------------
    # 📦 Context
    # -------------------------------------------------------------
    context = {
        "players": players,
        "player_summary": player_summary,
        "chart_labels": json.dumps(chart_labels),
        "chart_loads": json.dumps(chart_loads),
        "chart_distances": json.dumps(chart_distances),
        "chart_sprints": json.dumps(chart_sprints),
        "avg_load": round(avg_load, 1),
        "avg_distance": round(avg_distance, 1),
        "avg_sprints": round(avg_sprints, 1),

        "selected_player": selected_player,
        "trend_labels": json.dumps(trend_labels),
        "trend_loads": json.dumps(trend_loads),
        "trend_sprints": json.dumps(trend_sprints),

        "weeks": json.dumps(weeks),
        "acute_values": json.dumps(acute_values),
        "chronic_values": json.dumps(chronic_values),
        "selected_metric": selected_metric,

        # ⭐ Tabellen data
        "all_training_data": all_training_data,   # ruwe data per sessie
        "training_data": training_data,           # geaggregeerde weekdata + ACWR

        "active_page": "training",
    }

    return render(request, "Training.html", context)


def wedstrijddata(request):
    import json
    from django.db.models import Max, Sum
    from .models import WedstrijdData, Player

    # ---------- TARGET WAARDEN PER POSITIE ----------
    POSITION_TARGETS = {
        "Spits": {"km": 11.5, "hir": 950, "his": 200, "a_d": 180},
        "Targetman": {"km": 11, "hir": 500, "his": 75, "a_d": 160},
        "Buitenspeler": {"km": 11, "hir": 1000, "his": 150, "a_d": 150},
        "Dynamische middenvelder": {"km": 12, "hir": 950, "his": 200, "a_d": 180},
        "Controlerende middenvelder": {"km": 12, "hir": 700, "his": 150, "a_d": 180},
        "Centrale verdediger": {"km": 10.5, "hir": 500, "his": 100, "a_d": 160},
        "Vleugelverdediger": {"km": 11, "hir": 1000, "his": 250, "a_d": 190},
    }

    # ---------- SPELER SELECTIE ----------
    players = Player.objects.all().order_by("name")
    selected_player_name = request.GET.get("player")
    selected_player = (
        Player.objects.filter(name=selected_player_name).first()
        if selected_player_name else None
    )

    # ---------- LAATSTE 5 WEDSTRIJDEN ----------
    match_queryset = WedstrijdData.objects.all().order_by("-week")
    if selected_player:
        match_queryset = match_queryset.filter(player=selected_player)

    last_5_matches = list(match_queryset[:5][::-1])  # reversed ascending

    # ---------- STATISTIEKEN ----------
    if last_5_matches:
        avg_stats = {
            "avg_distance": sum(m.total_distance for m in last_5_matches) / len(last_5_matches),
            "avg_hsd":      sum(m.hsd for m in last_5_matches) / len(last_5_matches),
            "avg_sprints":  sum(m.sprints for m in last_5_matches) / len(last_5_matches),
            "avg_load":     sum(m.load for m in last_5_matches) / len(last_5_matches),
        }
        top_stats = {
            "top_distance": max(m.total_distance for m in last_5_matches),
            "top_hsd":      max(m.hsd for m in last_5_matches),
            "top_sprints":  max(m.sprints for m in last_5_matches),
            "top_load":     max(m.load for m in last_5_matches),
        }
    else:
        avg_stats, top_stats = {}, {}

    # ---------- POSITION TARGETS ----------
    position_targets = (
        POSITION_TARGETS.get(selected_player.position)
        if selected_player else None
    )

    # ---------- MATCH GRAFIEKEN ----------
    match_labels = [f"WK {m.week}" for m in last_5_matches]
    match_km      = [float(m.total_distance or 0) for m in last_5_matches]
    match_hir     = [float(m.hsd or 0) for m in last_5_matches]
    match_his     = [float(m.sprints or 0) for m in last_5_matches]
    match_load    = [float(m.load or 0) for m in last_5_matches]

    # =======================================================================
    # ⭐ TEAMVERGELIJKING — UNIEKE SPELERS ⭐
    # =======================================================================

        # --- LAATSTE WEEK OPHALEN ---
    result = WedstrijdData.objects.aggregate(max_week=Max("week"))
    last_week = result["max_week"]

    # Als er geen week beschikbaar is → lege grafiek
    if not last_week:
        last_team_rows = []
    else:
        last_team_rows = (
            WedstrijdData.objects
                .filter(week=last_week)
                .values("player__name")
                .annotate(
                    km=Sum("total_distance"),   # totale afstand (meters)
                    hir=Sum("hsd"),             # high-intensity running (meters)
                    sprints=Sum("sprints"),     # aantal sprints
                    his=Sum("his"),             # high-intensity sprint distance (meters)
                )
                .order_by("player__name")
        )

 # TEAM DATA ARRAYS
    team_labels   = [row["player__name"] for row in last_team_rows]
    team_distance = [float(row["km"] or 0) for row in last_team_rows]
    team_hsd      = [float(row["hir"] or 0) for row in last_team_rows]
    team_sprints  = [float(row["sprints"] or 0) for row in last_team_rows]
    team_his      = [float(row["his"] or 0) for row in last_team_rows]

    # ---------- CONTEXT ----------
    context = {
        "players": players,
        "selected_player": selected_player,
        "last_5_matches": last_5_matches,
        "avg_stats": avg_stats,
        "top_stats": top_stats,
        "targets": position_targets,

        "match_labels": match_labels,
        "match_km": match_km,
        "match_hir": match_hir,
        "match_his": match_his,
        "match_load": match_load,

        "team_labels": team_labels,
        "team_distance": team_distance,
        "team_hsd": team_hsd,
        "team_sprints": team_sprints,
        "team_his": team_his,

        "active_page": "wedstrijd",
    }

    return render(request, "Training.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Min, Max
from .models import Player, PlayerTest


def testdata(request):

    # ----------------------------------------------------------
    # Percentiel functie
    # ----------------------------------------------------------
    def calculate_percentile(value, min_val, max_val, reverse=False):
        """Bereken percentiel t.o.v. team. reverse=True = lager is beter (sprint)."""
        if value is None or min_val is None or max_val is None:
            return None
        if min_val == max_val:
            return 50  # fallback wanneer er weinig data is

        if reverse:
            # Sprint → lager = beter
            return round(100 * (max_val - value) / (max_val - min_val))
        else:
            # CMJ / ISRT / submax → hoger = beter
            return round(100 * (value - min_val) / (max_val - min_val))

    # ============================================
    # 1. Teamdata ophalen (voor teamgrafiek + percentielen)
    # ============================================
    players = Player.objects.all().order_by("name")
    test_data = PlayerTest.objects.select_related("player").all()

    team_min = test_data.aggregate(
        sprint10_min=Min("sprint_10"),
        sprint30_min=Min("sprint_30"),
        cmj_min=Min("cmj"),
        isrt_min=Min("isrt"),
        submax_min=Min("submax"),
    )

    team_max = test_data.aggregate(
        sprint10_max=Max("sprint_10"),
        sprint30_max=Max("sprint_30"),
        cmj_max=Max("cmj"),
        isrt_max=Max("isrt"),
        submax_max=Max("submax"),
    )

    # ============================================
    # 2. Spelerselectie + percentielen
    # ============================================
    player_id = request.GET.get("player_id")
    selected_player = None
    percentiles = {}

    if player_id:
        selected_player = get_object_or_404(Player, id=player_id)

        # Haal nieuwste test op obv test_date
        latest_test = (
            PlayerTest.objects
            .filter(player=selected_player)
            .order_by("-test_date")
            .first()
        )
        selected_player.latest_test = latest_test

        if latest_test:
            percentiles = {
                "sprint_10": calculate_percentile(
                    latest_test.sprint_10,
                    team_min["sprint10_min"],
                    team_max["sprint10_max"],
                    reverse=True
                ),
                "sprint_30": calculate_percentile(
                    latest_test.sprint_30,
                    team_min["sprint30_min"],
                    team_max["sprint30_max"],
                    reverse=True
                ),
                "cmj": calculate_percentile(
                    latest_test.cmj,
                    team_min["cmj_min"],
                    team_max["cmj_max"]
                ),
                "isrt": calculate_percentile(
                    latest_test.isrt,
                    team_min["isrt_min"],
                    team_max["isrt_max"]
                ),
                "submax": calculate_percentile(
                    latest_test.submax,
                    team_min["submax_min"],
                    team_max["submax_max"]
                ),
            }

    # ============================================
    # 2b. Trendgrafiek data (sorted op test_date)
    # ============================================
    if player_id:
        tests = PlayerTest.objects.filter(player=selected_player).order_by("test_date")

        anthropometry_dates = [t.test_date.strftime("%d-%m-%Y") for t in tests]

        # FORWARD FILL – Gewicht
        anthropometry_weights = []
        last_weight = None
        for t in tests:
            if t.curr_weight is not None:
                last_weight = t.curr_weight
            anthropometry_weights.append(last_weight)

        # FORWARD FILL – Skinfolds
        anthropometry_skinfolds = []
        last_skin = None
        for t in tests:
            if t.sum_skinfolds is not None:
                last_skin = t.sum_skinfolds
            anthropometry_skinfolds.append(last_skin)

    # ============================================
    # 3. Teamgemiddelden
    # ============================================
    team_avg = {
        "sprint_10": round(test_data.aggregate(Avg("sprint_10"))["sprint_10__avg"] or 0, 2),
        "sprint_30": round(test_data.aggregate(Avg("sprint_30"))["sprint_30__avg"] or 0, 2),
        "cmj": round(test_data.aggregate(Avg("cmj"))["cmj__avg"] or 0, 2),
        "isrt": round(test_data.aggregate(Avg("isrt"))["isrt__avg"] or 0, 2),
        "submax": round(test_data.aggregate(Avg("submax"))["submax__avg"] or 0, 2),
    }

    # ============================================
    # 4. Nieuwe testdata opslaan (POST)
    # ============================================
    if request.method == "POST":
        player_obj = get_object_or_404(Player, id=request.POST.get("player_id"))
        test_date = request.POST.get("test_date")  # komt uit formulier (input type="date")

        PlayerTest.objects.create(
            player=player_obj,
            test_date=test_date,
            sprint_10=request.POST.get("sprint_10") or None,
            sprint_30=request.POST.get("sprint_30") or None,
            cmj=request.POST.get("cmj") or None,
            isrt=request.POST.get("isrt") or None,
            submax=request.POST.get("submax") or None,
            curr_weight=request.POST.get("curr_weight") or None,
            length=request.POST.get("length") or None,
            sum_skinfolds=request.POST.get("sum_skinfolds") or None,
        )

        return redirect("testdata")

    # ============================================
    # 5. Context bouwen (incl. test_data voor teamgrafiek)
    # ============================================
    context = {
        "players": players,
        "selected_player": selected_player,
        "test_data": test_data,          # 🔥 deze wordt gebruikt in je verborgen tabel #hiddenData
        "team_avg": team_avg,
        "percentiles": percentiles,
    }

    if player_id:
        context.update({
            "anthropometry_dates": anthropometry_dates,
            "anthropometry_weights": anthropometry_weights,
            "anthropometry_skinfolds": anthropometry_skinfolds,
        })

    return render(request, "testdata.html", context)


# ---------- PAGINA: HERSTEL ----------
def recovery(request):
    """Pagina voor herstel- en testanalyse per speler."""
    players = Player.objects.all().order_by("name")
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
from .models import Injury, Player, FieldRehabSession

def revalidatie(request):
    """Pagina voor overzicht van geblesseerde spelers + invoer van veldrevalidatie."""
    injuries = Injury.objects.all().order_by("start_date")
    players = Player.objects.all().order_by("name")

    selected_player_name = request.GET.get("player")
    selected_player = None

    if selected_player_name:
        selected_player = Player.objects.filter(name=selected_player_name).first()
        if selected_player:
            injuries = Injury.objects.filter(name=selected_player.name).order_by("start_date")
        else:
            injuries = []

    # 👇 Nieuw deel – formulierverwerking
    if request.method == "POST":
        player_id = request.POST.get("player")
        phase = request.POST.get("phase")

        # ✅ Haal lijsten op (door de [] in de HTML)
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

            # ✅ Doorloop alle rijen in de tabel
            for i in range(len(onderdelen)):
                onderdeel = onderdelen[i].strip() if onderdelen[i] else None
                if not onderdeel:
                    continue  # sla lege rijen over

                FieldRehabSession.objects.create(
                    player=player,
                    phase=phase,
                    onderdeel=onderdeel,
                    afgevinkt=True if i < len(afgevinkts) and afgevinkts[i] == "on" else False,
                    duur=duuren[i] if i < len(duuren) and duuren[i] else None,
                    rpe=rpes[i] if i < len(rpes) and rpes[i] else None,
                    totale_afstand=totale_afstanden[i] if i < len(totale_afstanden) and totale_afstanden[i] else None,
                    afstand_20=afstand_20s[i] if i < len(afstand_20s) and afstand_20s[i] else None,
                    afstand_25=afstand_25s[i] if i < len(afstand_25s) and afstand_25s[i] else None,
                    acceleraties=acceleraties[i] if i < len(acceleraties) and acceleraties[i] else None,
                    deceleraties=deceleraties[i] if i < len(deceleraties) and deceleraties[i] else None,
                )

        except Player.DoesNotExist:
            print("⚠️ Ongeldige speler geselecteerd")

        return redirect("revalidatie")

    # 👇 Context teruggeven aan template
    context = {
        "injuries": injuries,
        "players": players,
        "selected_player": selected_player,
    }

    return render(request, "revalidatie.html", context)

def revalidatie_gym(request):
    """Pagina voor oefeningen en voortgang in de revalidatiegym."""
    if request.method == "POST":
        player = request.POST.get("player")
        phase = request.POST.get("phase")
        exercise = request.POST.get("exercise")
        description = request.POST.get("description")
        sets_reps = request.POST.get("sets_reps")

        # ✅ Eerst proberen de juiste speler op te halen
        try:
            player_obj = Player.objects.get(name=player)
        except Player.DoesNotExist:
            player_obj = None

        # ✅ Dan de oefening aanmaken met de juiste ForeignKey
        Oefening.objects.create(
            player=player_obj,
            phase=phase,
            exercise=exercise,
            description=description,
            sets_reps=sets_reps
        )

        return redirect("revalidatie_gym")

    # ✅ Deze code moet BUITEN de if staan, zodat ze ook bij GET uitgevoerd wordt
    oefeningen = Oefening.objects.all().order_by("-created_at")
    spelers = Player.objects.all().order_by("name")  # <--- deze regel ontbrak!

    # ✅ Geef beide variabelen door aan de template
    return render(request, "revalidatie_gym.html", {
        "oefeningen": oefeningen,
        "spelers": spelers,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date

from .models import Player, Programma, ProgrammaOefening, DailyProgram, RPEEntry

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

    players = Player.objects.all().order_by("name")

    # Haal geselecteerde speler uit URL parameters
    player_id = request.GET.get("player_id")
    selected_player = None
    programma = None
    oefeningen = []
    day_program = None

    if player_id:
        selected_player = get_object_or_404(Player, id=player_id)

        # Dagprogramma ophalen of aanmaken
        day_program, created = DailyProgram.objects.get_or_create(
            player=selected_player,
            date=date.today()
        )

        # Laatste individuele programma ophalen
        programma = Programma.objects.filter(player=selected_player).order_by("-created_at").first()

        if programma:
            oefeningen = ProgrammaOefening.objects.filter(programma=programma)

        # Opslaan dagprogramma
        if request.method == "POST":
            new_text = request.POST.get("program_text", "")
            day_program.program_text = new_text
            day_program.save()
            messages.success(request, "Dagprogramma opgeslagen!")
            return redirect(f"/individuele_programmas/?player_id={player_id}")

    context = {
        "players": players,
        "selected_player": selected_player,
        "day_program": day_program,
        "programma": programma,
        "oefeningen": oefeningen,
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

        programma = Programma.objects.create(
            player=player,
            doel=doel,
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
                ProgrammaOefening.objects.create(
                    programma=programma,
                    naam=name,
                    duur=duur,
                    rpe=rpe,
                    frequentie=freq,
                    opmerkingen=notes
                )

        messages.success(request, f"Programma voor {player.name} succesvol opgeslagen!")
        return redirect(f"/individuele_programmas/?player_id={player.id}")

    return redirect("individuele_programmas")

def rpe_view(request):
    """
    RPE-pagina met dezelfde structuur als Wellness:
    → toont 'niet ingevuld' en 'wel ingevuld' voor vandaag.
    """

    # --- Alle spelers ---
    players = Player.objects.all().order_by("name")

    # --- Datum filter (vandaag) ---
    today = timezone.now().date()

    # --- Alle ingevulde RPE’s van vandaag ---
    todays_rpe = RPEEntry.objects.filter(date=today)

    # --- Lijsten voor UI ---
    players_with_rpe = {entry.player.id for entry in todays_rpe}  # set van player IDs

    not_filled = [p for p in players if p.id not in players_with_rpe]
    filled = todays_rpe.order_by("player__name")

    # --- POST → RPE opslaan ---
    if request.method == "POST":
        player_id = request.POST.get("player_id")
        rpe_value = request.POST.get("rpe")
        training_type = request.POST.get("training_type")
        date_value = request.POST.get("date")

        player = get_object_or_404(Player, id=player_id)

        # Geen datum → vandaag
        if not date_value:
            date_value = today

        # Bestaat er al een rpe entry voor die speler vandaag?
        existing = RPEEntry.objects.filter(player=player, date=date_value).first()

        if existing:
            # Updaten
            existing.training_type = training_type
            existing.rpe = rpe_value
            existing.save()
        else:
            # Nieuwe entry
            RPEEntry.objects.create(
                player=player,
                date=date_value,
                training_type=training_type,
                rpe=rpe_value
            )

        return redirect("/rpe/")

    context = {
        "players": players,
        "today": today,
        "not_filled": not_filled,   # spelers die nog geen RPE hebben
        "filled": filled,           # ingevulde RPE entries
    }

    return render(request, "rpe.html", context)

def wellness(request):
    """Wellness dashboard met onderscheid tussen ingevuld en niet ingevuld."""

    # 1️⃣ Datum ophalen & converteren naar date-object
    selected_date = request.GET.get("date")

    if selected_date:
        # GET levert een string -> converteren naar date
        date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        date = timezone.now().date()

    # 2️⃣ Spelers ophalen
    players = Player.objects.all().order_by("name")

    # 3️⃣ Entries van deze datum ophalen
    existing_entries = WellnessEntry.objects.filter(date=date)

    filled_player_ids = set(existing_entries.values_list("player_id", flat=True))

    # 4️⃣ Verdeling in ingevuld / niet ingevuld
    players_filled = [p for p in players if p.id in filled_player_ids]
    players_not_filled = [p for p in players if p.id not in filled_player_ids]

    # 5️⃣ POST: wellness opslaan
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

    # 6️⃣ Context + render
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
from .models import HitWeekPlanning


def hit_page(request):
    """
    HIT pagina: toont tools + slaat weekplanning op wanneer een POST-request binnenkomt.
    """

    # Pak het algemene record (ID=1), of maak deze automatisch aan
    weekplanning, created = HitWeekPlanning.objects.get_or_create(id=1)

    if request.method == "POST":

        # Velden ophalen en opslaan
        weekplanning.monday = request.POST.get("maandag", "")
        weekplanning.tuesday = request.POST.get("dinsdag", "")
        weekplanning.wednesday = request.POST.get("woensdag", "")
        weekplanning.thursday = request.POST.get("donderdag", "")
        weekplanning.friday = request.POST.get("vrijdag", "")
        weekplanning.saturday = request.POST.get("zaterdag", "")
        weekplanning.sunday = request.POST.get("zondag", "")

        weekplanning.save()

        messages.success(request, "HIT-weekplanning opgeslagen ✔️")

        # voorkomt dubbel-submit bij refresh
        return redirect("hit_page")

    # GET → render pagina + huidige planning values
    return render(request, "hit.html", {"weekplanning": weekplanning})




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
    players = Player.objects.all().order_by("name")

    # 3. Voor elke speler een Aanwezigheid entry ophalen of automatisch aanmaken
    records = []
    for player in players:
        aanwezigheid, created = Aanwezigheid.objects.get_or_create(
            player=player,
            date=chosen_date,
            defaults={"status": "overig", "completed": False}
        )
        records.append(aanwezigheid)

    # 4. Navigatie (vorige dag / volgende dag)
    previous_day = chosen_date - timedelta(days=1)
    next_day = chosen_date + timedelta(days=1)

    context = {
        "players": players,
        "records": records,
        "chosen_date": chosen_date,
        "previous_day": previous_day,
        "next_day": next_day,
        "status_choices": Aanwezigheid.STATUS_OPTIES,
    }

    return render(request, "aanwezigheden.html", context)


# -------------------------------------
# AANWEZIGHEDEN UPDATE
# -------------------------------------
def aanwezigheden_update(request, record_id):
    """Update één aanwezigheidsrecord (dropdown + checkmark)."""

    aanwezigheid = get_object_or_404(Aanwezigheid, id=record_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        completed = request.POST.get("completed") == "on"

        aanwezigheid.status = new_status
        aanwezigheid.completed = completed
        aanwezigheid.save()

        messages.success(
            request,
            f"Aanwezigheid bijgewerkt voor {aanwezigheid.player.name}"
        )

    return redirect(f"/aanwezigheden/?date={aanwezigheid.date}")


def overig(request):
    page = request.GET.get('page', 'menu')

    staff_members = Staff.objects.all().order_by('name')
    players = Player.objects.all().order_by('name')

    # ======================================
    # NOTITIES
    # ======================================
    if page == "notities":
        if request.method == 'POST':
            text = request.POST.get('text')
            Overig.objects.create(text=text)
            return redirect('/overig/?page=notities')

        items = Overig.objects.all().order_by('-created_at')
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
        return render(request, 'overig.html', {
            'page': 'hp',
            'players': players,
            'staff': staff_members,
        })

    # ======================================
    # JEUGD WILLEM II
    # ======================================
    if page == "jeugd":
        return render(request, 'overig.html', {
            'page': 'jeugd',
            'players': players,
            'staff': staff_members,
        })

    # ======================================
    # DEFAULT → MENU
    # ======================================
    return render(request, 'overig.html', {
        'page': 'menu',
        'players': players,
        'staff': staff_members,
    })


def player_data(request, player_id):
    """
    Geeft JSON terug met de voortgang van gewicht en huidplooien
    voor één specifieke speler. Wordt aangeroepen als je op een speler klikt.
    """
    from .models import Player, PlayerTest

    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({'error': 'Speler niet gevonden'}, status=404)

    # 📊 Testdata ophalen (bijv. metingen uit PlayerTest)
    tests = PlayerTest.objects.filter(name=player.name).order_by('created_at')

    # Als er nog geen testdata zijn → laat een eenvoudige trend zien
    if not tests.exists():
        data = {
            'dates': ["Week 1", "Week 2", "Week 3", "Week 4"],
            'weights': [
                float(player.prev_weight or 0),
                float((player.prev_weight or 0) * 0.99),
                float(player.curr_weight or 0),
                float((player.curr_weight or 0) * 1.01),
            ],
            'skinfolds': [
                float(player.sum_skinfolds or 0),
                float((player.sum_skinfolds or 0) * 0.98),
                float(player.sum_skinfolds or 0),
                float((player.sum_skinfolds or 0) * 1.02),
            ]
        }
        return JsonResponse(data)

    # ✅ Echte data gebruiken uit PlayerTest
    dates = [t.created_at.strftime("%d-%m-%Y") for t in tests]
    weights = [float(t.curr_weight or 0) for t in tests]
    skinfolds = [float(t.sum_skinfolds or 0) for t in tests]

    data = {
        'dates': dates,
        'weights': weights,
        'skinfolds': skinfolds
    }
    return JsonResponse(data)
    
# ---------- DATA-UPLOAD (CSV) ----------
from django.shortcuts import redirect
from django.contrib import messages
import csv
from datetime import datetime
from .models import Player, TrainingData


def upload_file(request):
    """Uploadt een StatsSports CSV en slaat de data correct op in TrainingData."""
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, '❌ Upload een geldig CSV-bestand (.csv).')
            return redirect('training')

        # CSV lezen
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        print("📄 CSV kolommen gedetecteerd:", reader.fieldnames)

        # Helpers
        def safe_float(value):
            try:
                return float(value)
            except:
                return 0.0

        def safe_int(value):
            try:
                return int(float(value))
            except:
                return 0

        count = 0

        for row in reader:
            try:
                # -----------------------------
                # 1. Speler zoeken op achternaam
                # -----------------------------
                csv_lastname = (row.get('Player Last Name') or "").replace('"', '').strip().lower()

                if not csv_lastname:
                    print("⚠️ Rij overgeslagen: geen achternaam gevonden")
                    continue

                # Zoek speler door laatste naamdeel uit volledig naamveld te vergelijken
                player = None
                for p in Player.objects.all():
                    full = p.name.lower().strip()
                    db_lastname = full.split()[-1]  # laatste woord = achternaam

                    if db_lastname == csv_lastname:
                        player = p
                        break

                if not player:
                    print(f"⚠️ Geen speler gevonden voor achternaam: '{csv_lastname}'")
                    continue

                # -----------------------------
                # 2. Datum omzetten
                # -----------------------------
                date_raw = (row.get('Session Date') or "").replace('"', '').strip()

                try:
                    date_obj = datetime.strptime(date_raw, "%d/%m/%Y").date()
                except:
                    print(f"⚠️ Ongeldig datumformaat: '{date_raw}'")
                    continue

                week = date_obj.isocalendar()[1]

                # -----------------------------
                # 3. Dubbele invoer voorkomen
                # -----------------------------
                if TrainingData.objects.filter(player=player, session_date=date_obj).exists():
                    print(f"⏭️ Al aanwezig: {player.name} - {date_obj}")
                    continue

                # -----------------------------
                # 4. Metrics veilig uitlezen
                # -----------------------------
                total_distance = safe_float(row.get('Total Distance'))
                hsd = safe_float(row.get('HIR (M>20 KM/U)'))
                sprints = safe_int(row.get('Sprints'))

                # Geen Session Load in jouw CSV
                load = 0

                # -----------------------------
                # 5. Opslaan in DB
                # -----------------------------
                TrainingData.objects.create(
                    player=player,
                    session_date=date_obj,
                    week=week,
                    total_distance=total_distance,
                    hsd=hsd,
                    sprints=sprints,
                    load=load,
                )

                count += 1

            except Exception as e:
                print(f"❌ Fout bij verwerken rij: {e}")
                continue

        messages.success(request, f"✅ {count} trainingsregels succesvol geïmporteerd.")
        return redirect('training')

    return redirect('training')



def upload_wedstrijddata(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "❌ Upload een geldig CSV-bestand (.csv).")
            return redirect('training')

        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded, skipinitialspace=True)

        print("📄 CSV kolommen gedetecteerd:", reader.fieldnames)

        def safe_float(v):
            try: return float(v)
            except: return 0.0

        def safe_int(v):
            try: return int(float(v))
            except: return 0

        count = 0

        for row in reader:
            try:
                # -----------------------------------
                # 1. ACHTERNAAM uit CSV
                # -----------------------------------
                csv_lastname = (row.get("Player Last Name") or "").strip().lower()
                if not csv_lastname:
                    continue

                # Normaliseer speciale tekens zoals Č -> c
                csv_lastname = csv_lastname.replace("č", "c").replace("ć", "c").replace("š", "s")

                # -----------------------------------
                # 2. MATCH SPELER OP ACHTERNAAM
                #    → CSV-achternaam moet ergens in Player.name voorkomen
                # -----------------------------------
                player = None
                for p in Player.objects.all():
                    name_clean = p.name.lower().replace("č", "c").replace("ć", "c").replace("š", "s")
                    if csv_lastname in name_clean:
                        player = p
                        break

                if not player:
                    print(f"⚠️ Geen speler gevonden op basis van achternaam: {csv_lastname}")
                    continue

                # -----------------------------------
                # 3. DATUM
                # -----------------------------------
                raw_date = (row.get("Session Date") or "").strip()

                try:
                    match_date = datetime.strptime(raw_date, "%d/%m/%Y").date()
                except:
                    print("⚠️ Ongeldige datum:", raw_date)
                    continue

                week = match_date.isocalendar()[1]

                # -----------------------------------
                # 4. CHECK DUBBEL
                # -----------------------------------
                if WedstrijdData.objects.filter(player=player, match_date=match_date).exists():
                    print("⏭️ Al aanwezig:", player.name, match_date)
                    continue

                # -----------------------------------
                # 5. METRICS
                # -----------------------------------
                acc = safe_int(row.get("Accelerations (Absolute)"))
                dec = safe_int(row.get("Decelerations (Absolute)"))
                hsd = safe_float(row.get("HIR (M>20 KM/U)"))
                his = safe_float(row.get("HIS (M>25 KM/U)"))
                total_distance = safe_float(row.get("Total Distance"))
                sprints = safe_int(row.get("Sprints"))
                load = safe_float(row.get("HML Distance"))

                # -----------------------------------
                # 6. OPSLAAN
                # -----------------------------------
                WedstrijdData.objects.create(
                    player=player,
                    match_date=match_date,
                    week=week,
                    accelerations=acc,
                    decelerations=dec,
                    hsd=hsd,
                    his=his,
                    total_distance=total_distance,
                    sprints=sprints,
                    load=load,
                )

                count += 1

            except Exception as e:
                print("❌ Fout:", e)
                continue

        messages.success(request, f"✅ {count} wedstrijdregels geïmporteerd.")
        return redirect('training')

    return redirect('training')
