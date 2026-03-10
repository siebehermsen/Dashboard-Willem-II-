from django.db import migrations, models


def forwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    for oef in ProgrammaOefening.objects.all().iterator():
        raw = getattr(oef, "rpe", None)
        if raw in (None, ""):
            continue
        try:
            parsed = int(str(raw).strip())
        except (TypeError, ValueError):
            parsed = None
        if parsed is None:
            continue
        oef.rpe_value = parsed
        oef.save(update_fields=["rpe_value"])


def backwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    for oef in ProgrammaOefening.objects.all().iterator():
        if oef.rpe_value is None:
            continue
        oef.rpe = str(oef.rpe_value)
        oef.save(update_fields=["rpe"])


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0067_programma_oefening_frequentie_lookup_3nf"),
    ]

    operations = [
        migrations.AddField(
            model_name="programmaoefening",
            name="rpe_value",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="programmaoefening",
            name="rpe",
        ),
    ]
