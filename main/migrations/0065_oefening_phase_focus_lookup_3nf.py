from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    Oefening = apps.get_model("main", "Oefening")
    OefeningProgramType = apps.get_model("main", "OefeningProgramType")
    OefeningPhase = apps.get_model("main", "OefeningPhase")
    OefeningFocusPoint = apps.get_model("main", "OefeningFocusPoint")

    pt_cache = {}
    phase_cache = {}
    fp_cache = {}

    for row in Oefening.objects.all().order_by("id"):
        update_fields = []

        raw_phase = (getattr(row, "phase", None) or "").strip()
        if raw_phase:
            program_type_text = None
            phase_text = raw_phase
            if " | " in raw_phase:
                program_type_text, phase_text = [p.strip() for p in raw_phase.split(" | ", 1)]

            if program_type_text:
                obj = pt_cache.get(program_type_text)
                if obj is None:
                    obj, _ = OefeningProgramType.objects.get_or_create(
                        name=program_type_text,
                        defaults={"is_active": True},
                    )
                    pt_cache[program_type_text] = obj
                row.program_type_ref_id = obj.id
                update_fields.append("program_type_ref")

            if phase_text:
                obj = phase_cache.get(phase_text)
                if obj is None:
                    obj, _ = OefeningPhase.objects.get_or_create(
                        name=phase_text,
                        defaults={"is_active": True},
                    )
                    phase_cache[phase_text] = obj
                row.phase_ref_id = obj.id
                update_fields.append("phase_ref")

        raw_focus = (getattr(row, "focus_point", None) or "").strip()
        if raw_focus:
            obj = fp_cache.get(raw_focus)
            if obj is None:
                obj, _ = OefeningFocusPoint.objects.get_or_create(
                    name=raw_focus,
                    defaults={"is_active": True},
                )
                fp_cache[raw_focus] = obj
            row.focus_point_ref_id = obj.id
            update_fields.append("focus_point_ref")

        if update_fields:
            row.save(update_fields=sorted(set(update_fields)))


def backwards(apps, schema_editor):
    # No-op: legacy text fields are removed in this migration.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0064_player_position_staff_role_lookup_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="OefeningFocusPoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="OefeningPhase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="OefeningProgramType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="oefening",
            name="focus_point_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="oefeningen",
                to="main.oefeningfocuspoint",
                verbose_name="Aandachtspunt",
            ),
        ),
        migrations.AddField(
            model_name="oefening",
            name="phase_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="oefeningen",
                to="main.oefeningphase",
                verbose_name="Fase",
            ),
        ),
        migrations.AddField(
            model_name="oefening",
            name="program_type_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="oefeningen",
                to="main.oefeningprogramtype",
                verbose_name="Programmatype",
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(model_name="oefening", name="focus_point"),
        migrations.RemoveField(model_name="oefening", name="phase"),
        migrations.AddIndex(
            model_name="oefening",
            index=models.Index(fields=["program_type_ref", "phase_ref"], name="main_oefeni_program_9e8be1_idx"),
        ),
    ]
