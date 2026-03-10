from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    FieldRehabSession = apps.get_model("main", "FieldRehabSession")
    FieldRehabPhase = apps.get_model("main", "FieldRehabPhase")
    FieldRehabComponent = apps.get_model("main", "FieldRehabComponent")

    phase_cache = {}
    component_cache = {}

    for row in FieldRehabSession.objects.all().order_by("id"):
        update_fields = []

        phase_name = (getattr(row, "phase", None) or "").strip()
        if phase_name:
            obj = phase_cache.get(phase_name)
            if obj is None:
                obj, _ = FieldRehabPhase.objects.get_or_create(
                    name=phase_name,
                    defaults={"is_active": True},
                )
                phase_cache[phase_name] = obj
            row.phase_ref_id = obj.id
            update_fields.append("phase_ref")

        component_name = (getattr(row, "onderdeel", None) or "").strip()
        if component_name:
            obj = component_cache.get(component_name)
            if obj is None:
                obj, _ = FieldRehabComponent.objects.get_or_create(
                    name=component_name,
                    defaults={"is_active": True},
                )
                component_cache[component_name] = obj
            row.onderdeel_ref_id = obj.id
            update_fields.append("onderdeel_ref")

        if update_fields:
            row.save(update_fields=update_fields)


def backwards(apps, schema_editor):
    # No-op: legacy text fields are removed in this migration.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0060_merge_0059_injury_and_attendance"),
    ]

    operations = [
        migrations.CreateModel(
            name="FieldRehabComponent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="FieldRehabPhase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="fieldrehabsession",
            name="onderdeel_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="sessions",
                to="main.fieldrehabcomponent",
                verbose_name="Onderdeel",
            ),
        ),
        migrations.AddField(
            model_name="fieldrehabsession",
            name="phase_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="sessions",
                to="main.fieldrehabphase",
                verbose_name="Revalidatiefase",
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="fieldrehabsession",
            name="onderdeel",
        ),
        migrations.RemoveField(
            model_name="fieldrehabsession",
            name="phase",
        ),
        migrations.AddIndex(
            model_name="fieldrehabsession",
            index=models.Index(fields=["player", "created_at"], name="main_fieldr_player__f9d60d_idx"),
        ),
        migrations.AddIndex(
            model_name="fieldrehabsession",
            index=models.Index(fields=["phase_ref", "onderdeel_ref"], name="main_fieldr_phase_r_9f7c42_idx"),
        ),
    ]
