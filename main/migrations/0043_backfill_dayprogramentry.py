from django.db import migrations
from django.utils.dateparse import parse_date


def forwards(apps, schema_editor):
    DayProgram = apps.get_model("main", "DayProgram")
    DayProgramEntry = apps.get_model("main", "DayProgramEntry")

    for old in DayProgram.objects.all().order_by("id"):
        parsed = parse_date((old.date or "").strip()) if isinstance(old.date, str) else None
        if not parsed:
            continue

        # Gebruik title als stabiele sleutel voor de bestaande unique constraint.
        title = (old.activities or "").strip()[:120] or "Dagprogramma"

        obj, created = DayProgramEntry.objects.get_or_create(
            date=parsed,
            title=title,
            defaults={
                "activities": old.activities,
                "notes": old.notes,
            },
        )
        if not created:
            if not obj.activities and old.activities:
                obj.activities = old.activities
            if not obj.notes and old.notes:
                obj.notes = old.notes
            obj.save(update_fields=["activities", "notes"])


def backwards(apps, schema_editor):
    # No-op: geen automatische rollback naar legacy tabel.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0042_backfill_3nf_phase1_data"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

