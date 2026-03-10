from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    RPEEntry = apps.get_model("main", "RPEEntry")
    RPETrainingType = apps.get_model("main", "RPETrainingType")

    defaults = ["Training", "Wedstrijd", "Individueel"]
    cache = {}

    for name in defaults:
        obj, _ = RPETrainingType.objects.get_or_create(name=name, defaults={"is_active": True})
        cache[name] = obj

    for row in RPEEntry.objects.all().order_by("id"):
        type_name = (getattr(row, "training_type", None) or "").strip()
        if not type_name:
            continue
        obj = cache.get(type_name)
        if obj is None:
            obj, _ = RPETrainingType.objects.get_or_create(
                name=type_name,
                defaults={"is_active": True},
            )
            cache[type_name] = obj
        row.training_type_ref_id = obj.id
        row.save(update_fields=["training_type_ref"])


def backwards(apps, schema_editor):
    # No-op: legacy text field is removed in this migration.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0061_fieldrehabsession_lookup_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="RPETrainingType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="rpeentry",
            name="training_type_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="entries",
                to="main.rpetrainingtype",
                verbose_name="Trainingstype",
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="rpeentry",
            name="training_type",
        ),
        migrations.AddIndex(
            model_name="rpeentry",
            index=models.Index(fields=["training_type_ref", "date"], name="main_rpeent_trainin_a0f54b_idx"),
        ),
    ]
