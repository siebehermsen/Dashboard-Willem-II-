from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    InjuryCase = apps.get_model("main", "InjuryCase")
    InjuryType = apps.get_model("main", "InjuryType")
    InjuryPhase = apps.get_model("main", "InjuryPhase")
    InjuryStatus = apps.get_model("main", "InjuryStatus")

    phase_label_map = {
        "early": "Vroege fase",
        "mid": "Middenfase",
        "final": "Laatste fase",
    }
    status_label_map = {
        "active": "Actief",
        "closed": "Afgesloten",
    }

    phase_cache = {}
    status_cache = {}
    type_cache = {}

    for code, label in phase_label_map.items():
        obj, _ = InjuryPhase.objects.get_or_create(code=code, defaults={"label": label, "is_active": True})
        phase_cache[code] = obj

    for code, label in status_label_map.items():
        obj, _ = InjuryStatus.objects.get_or_create(code=code, defaults={"label": label, "is_active": True})
        status_cache[code] = obj

    for row in InjuryCase.objects.all().order_by("id"):
        update_fields = []

        injury_type_text = (getattr(row, "injury_type", None) or "").strip()
        if injury_type_text:
            obj = type_cache.get(injury_type_text)
            if obj is None:
                obj, _ = InjuryType.objects.get_or_create(
                    name=injury_type_text,
                    defaults={"is_active": True},
                )
                type_cache[injury_type_text] = obj
            row.injury_type_ref_id = obj.id
            update_fields.append("injury_type_ref")

        phase_code = (getattr(row, "phase", None) or "").strip()
        if phase_code:
            obj = phase_cache.get(phase_code)
            if obj is None:
                obj, _ = InjuryPhase.objects.get_or_create(
                    code=phase_code,
                    defaults={
                        "label": phase_label_map.get(phase_code, phase_code.replace("_", " ").title()),
                        "is_active": True,
                    },
                )
                phase_cache[phase_code] = obj
            row.phase_ref_id = obj.id
            update_fields.append("phase_ref")

        status_code = (getattr(row, "status", None) or "active").strip().lower()
        if status_code:
            obj = status_cache.get(status_code)
            if obj is None:
                obj, _ = InjuryStatus.objects.get_or_create(
                    code=status_code,
                    defaults={
                        "label": status_label_map.get(status_code, status_code.replace("_", " ").title()),
                        "is_active": True,
                    },
                )
                status_cache[status_code] = obj
            row.status_ref_id = obj.id
            update_fields.append("status_ref")

        if update_fields:
            row.save(update_fields=update_fields)


def backwards(apps, schema_editor):
    # No-op: this migration removes legacy text fields.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0058_match_team_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="InjuryPhase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=50, unique=True)),
                ("label", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["label"]},
        ),
        migrations.CreateModel(
            name="InjuryStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=30, unique=True)),
                ("label", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["label"]},
        ),
        migrations.CreateModel(
            name="InjuryType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="injurycase",
            name="injury_type_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="injury_cases",
                to="main.injurytype",
            ),
        ),
        migrations.AddField(
            model_name="injurycase",
            name="phase_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="injury_cases",
                to="main.injuryphase",
            ),
        ),
        migrations.AddField(
            model_name="injurycase",
            name="status_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="injury_cases",
                to="main.injurystatus",
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="injurycase",
            name="injury_type",
        ),
        migrations.RemoveField(
            model_name="injurycase",
            name="phase",
        ),
        migrations.RemoveField(
            model_name="injurycase",
            name="status",
        ),
        migrations.AddIndex(
            model_name="injurycase",
            index=models.Index(fields=["player", "status_ref"], name="main_injuryc_player__3nf_idx"),
        ),
    ]
