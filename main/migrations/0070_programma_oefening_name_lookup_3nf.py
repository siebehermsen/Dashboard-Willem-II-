from django.db import migrations, models


def forwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    ProgrammaOefeningNaam = apps.get_model("main", "ProgrammaOefeningNaam")

    cache = {}
    for oef in ProgrammaOefening.objects.all().iterator():
        raw = getattr(oef, "naam", None)
        if raw is None:
            continue
        text = str(raw).strip()
        if not text:
            continue
        if text not in cache:
            cache[text], _ = ProgrammaOefeningNaam.objects.get_or_create(name=text)
        oef.naam_ref_id = cache[text].id
        oef.save(update_fields=["naam_ref"])


def backwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    for oef in ProgrammaOefening.objects.select_related("naam_ref").all().iterator():
        if oef.naam_ref_id:
            oef.naam = oef.naam_ref.name
            oef.save(update_fields=["naam"])


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0069_programma_oefening_duur_structured_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgrammaOefeningNaam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="programmaoefening",
            name="naam_ref",
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name="programma_oefeningen", to="main.programmaoefeningnaam"),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="programmaoefening",
            name="naam",
        ),
        migrations.AddIndex(
            model_name="programmaoefening",
            index=models.Index(fields=["naam_ref"], name="main_progra_naam_re_44f130_idx"),
        ),
    ]
