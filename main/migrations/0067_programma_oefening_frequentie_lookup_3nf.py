from django.db import migrations, models


def forwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    ProgrammaFrequentie = apps.get_model("main", "ProgrammaFrequentie")

    cache = {}
    for oef in ProgrammaOefening.objects.all().iterator():
        raw = getattr(oef, "frequentie", None)
        if raw is None:
            continue
        text = str(raw).strip()
        if not text:
            continue
        if text not in cache:
            cache[text], _ = ProgrammaFrequentie.objects.get_or_create(name=text)
        oef.frequentie_ref_id = cache[text].id
        oef.save(update_fields=["frequentie_ref"])


def backwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    for oef in ProgrammaOefening.objects.select_related("frequentie_ref").all().iterator():
        if oef.frequentie_ref_id:
            oef.frequentie = oef.frequentie_ref.name
            oef.save(update_fields=["frequentie"])


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0066_fieldrehab_metrics_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgrammaFrequentie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="programmaoefening",
            name="frequentie_ref",
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name="oefeningen", to="main.programmafrequentie"),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="programmaoefening",
            name="frequentie",
        ),
        migrations.AddIndex(
            model_name="programmaoefening",
            index=models.Index(fields=["frequentie_ref"], name="main_progra_frequen_5b27e2_idx"),
        ),
    ]
