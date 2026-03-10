from datetime import timedelta
import re

from django.db import migrations


def _parse_duration_days(value):
    if value in (None, ""):
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if not text:
        return None
    match = re.search(r"\d+", text)
    if not match:
        return None
    try:
        return int(match.group(0))
    except (TypeError, ValueError):
        return None


def forwards(apps, schema_editor):
    Player = apps.get_model("main", "Player")
    Injury = apps.get_model("main", "Injury")
    InjuryCase = apps.get_model("main", "InjuryCase")
    HitWeekPlanning = apps.get_model("main", "HitWeekPlanning")
    HitWeekPlan = apps.get_model("main", "HitWeekPlan")
    HitWeekPlanEntry = apps.get_model("main", "HitWeekPlanEntry")

    # 1) Injury -> InjuryCase
    for old in Injury.objects.all().order_by("id"):
        player = Player.objects.filter(name=old.name).first()
        if player is None:
            player = Player.objects.filter(name__iexact=old.name).first()
        if player is None:
            continue

        duration_days = _parse_duration_days(old.duration)
        expected_return_on = None
        if old.start_date and duration_days is not None:
            expected_return_on = old.start_date + timedelta(days=duration_days)

        exists = InjuryCase.objects.filter(
            player=player,
            injury_type=old.injury_type,
            started_on=old.start_date,
            phase=old.phase,
        ).exists()
        if exists:
            continue

        InjuryCase.objects.create(
            player=player,
            injury_type=old.injury_type,
            phase=old.phase,
            status="active",
            started_on=old.start_date,
            expected_return_on=expected_return_on,
            notes="Backfill vanuit legacy Injury",
        )

    # 2) HitWeekPlanning -> HitWeekPlan / HitWeekPlanEntry
    old_plan = HitWeekPlanning.objects.order_by("-id").first()
    if old_plan is not None:
        new_plan, _ = HitWeekPlan.objects.get_or_create(name="Algemene HIT Weekplanning")
        day_values = {
            1: old_plan.monday or "",
            2: old_plan.tuesday or "",
            3: old_plan.wednesday or "",
            4: old_plan.thursday or "",
            5: old_plan.friday or "",
            6: old_plan.saturday or "",
            7: old_plan.sunday or "",
        }
        for day_of_week, content in day_values.items():
            entry, _ = HitWeekPlanEntry.objects.get_or_create(
                plan=new_plan,
                day_of_week=day_of_week,
                defaults={"content": content},
            )
            if not entry.content and content:
                entry.content = content
                entry.save(update_fields=["content"])


def backwards(apps, schema_editor):
    # Bewust no-op: we willen backfilled data niet automatisch verwijderen.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0041_rename_main_injuryc_player__8c0f5b_idx_main_injury_player__4e7bb7_idx_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

