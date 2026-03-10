from django.core.management.base import BaseCommand
from django.db.models import Count, Q

from main.models import (
    NutritionIntakeSession,
    PlayerSpeedTest,
    RPEEntry,
    WeightEntry,
    WellnessEntry,
)


class Command(BaseCommand):
    help = "Controleert kern-integriteit voor 3NF data-opslag."

    def handle(self, *args, **options):
        checks = []

        dup_nutrition = (
            NutritionIntakeSession.objects
            .exclude(date__isnull=True)
            .values("player_id", "date")
            .annotate(c=Count("id"))
            .filter(c__gt=1)
            .count()
        )
        checks.append(("Dubbele NutritionIntakeSession (player,date)", dup_nutrition))

        bad_rpe = RPEEntry.objects.filter(Q(rpe__lt=1) | Q(rpe__gt=10)).count()
        checks.append(("RPE buiten bereik 1..10", bad_rpe))

        bad_session_load = RPEEntry.objects.filter(session_load__lt=0).count()
        checks.append(("Negatieve RPE session_load", bad_session_load))

        bad_sleep = WellnessEntry.objects.filter(~Q(sleep__isnull=True) & (Q(sleep__lt=1) | Q(sleep__gt=5))).count()
        bad_mood = WellnessEntry.objects.filter(~Q(mood__isnull=True) & (Q(mood__lt=1) | Q(mood__gt=5))).count()
        bad_fit = WellnessEntry.objects.filter(~Q(fitness__isnull=True) & (Q(fitness__lt=1) | Q(fitness__gt=5))).count()
        bad_sore = WellnessEntry.objects.filter(~Q(soreness__isnull=True) & (Q(soreness__lt=1) | Q(soreness__gt=5))).count()
        checks.append(("Wellness score buiten bereik", bad_sleep + bad_mood + bad_fit + bad_sore))

        bad_mss = PlayerSpeedTest.objects.filter(mss_kmh__lte=0).count()
        bad_mas = PlayerSpeedTest.objects.filter(mas_kmh__lte=0).count()
        checks.append(("Snelheidstest met niet-positieve MSS/MAS", bad_mss + bad_mas))

        bad_weight = WeightEntry.objects.filter(weight__lte=0).count()
        checks.append(("Gewicht <= 0", bad_weight))

        self.stdout.write(self.style.SUCCESS("=== Data Integrity Check ==="))
        total_issues = 0
        for label, count in checks:
            total_issues += int(count)
            if count:
                self.stdout.write(self.style.WARNING(f"[WARN] {label}: {count}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"[OK] {label}: 0"))

        if total_issues:
            self.stdout.write(self.style.WARNING(f"Integriteit issues gevonden: {total_issues}"))
        else:
            self.stdout.write(self.style.SUCCESS("Geen integriteit issues gevonden."))
