from django.db import migrations


def _to_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def forwards(apps, schema_editor):
    Antropometry = apps.get_model("main", "Antropometry")
    AnthropometrySession = apps.get_model("main", "AnthropometrySession")
    AnthropometryMeasurement = apps.get_model("main", "AnthropometryMeasurement")

    skinfold_sites = [
        "triceps",
        "biceps",
        "subscapular",
        "iliac_crest",
        "supraspinale",
        "abdominal",
        "thigh",
        "calf",
    ]
    girth_sites = [
        "arm_relaxed",
        "arm_flexed",
        "thigh_girth",
        "calf_girth",
    ]

    for row in Antropometry.objects.all().order_by("id"):
        session, _ = AnthropometrySession.objects.get_or_create(
            player=row.player,
            date=row.date,
            defaults={
                "body_mass": row.body_mass,
                "length": row.length,
                "fat_dw": row.fat_dw,
                "fat_faulkner": row.fat_faulkner,
                "fat_carter": row.fat_carter,
                "fat_average": row.fat_average,
            },
        )

        # Bestaande meetpunten verwijderen voor idempotente backfill.
        AnthropometryMeasurement.objects.filter(session=session).delete()

        for site in skinfold_sites:
            for rep in (1, 2, 3):
                val = _to_float(getattr(row, f"{site}_m{rep}", None))
                if val is None:
                    continue
                AnthropometryMeasurement.objects.create(
                    session=session,
                    category="skinfold",
                    site_code=site,
                    repetition=rep,
                    value=val,
                )

        for site in girth_sites:
            for rep in (1, 2, 3):
                val = _to_float(getattr(row, f"{site}_m{rep}", None))
                if val is None:
                    continue
                AnthropometryMeasurement.objects.create(
                    session=session,
                    category="girth",
                    site_code=site,
                    repetition=rep,
                    value=val,
                )


def backwards(apps, schema_editor):
    # No-op: v2 data niet automatisch terugzetten naar legacy wide table.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0044_anthropometrysession_anthropometrymeasurement"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

