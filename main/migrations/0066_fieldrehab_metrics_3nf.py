from django.db import migrations, models


METRIC_DEFS = [
    ("duur", "Duur", "min"),
    ("rpe", "RPE", None),
    ("totale_afstand", "Totale afstand", "m"),
    ("afstand_20", "Afstand >20", "m"),
    ("afstand_25", "Afstand >25", "m"),
    ("acceleraties", "Acceleraties", None),
    ("deceleraties", "Deceleraties", None),
]


def forwards(apps, schema_editor):
    FieldRehabSession = apps.get_model("main", "FieldRehabSession")
    FieldRehabMetricType = apps.get_model("main", "FieldRehabMetricType")
    FieldRehabMetric = apps.get_model("main", "FieldRehabMetric")

    metric_types = {}
    for code, name, unit in METRIC_DEFS:
        metric_types[code], _ = FieldRehabMetricType.objects.get_or_create(
            code=code,
            defaults={"name": name, "unit": unit},
        )

    rows = []
    fields = [code for code, _, _ in METRIC_DEFS]
    for session in FieldRehabSession.objects.all().iterator():
        for code in fields:
            value = getattr(session, code, None)
            if value is None:
                continue
            rows.append(
                FieldRehabMetric(
                    session_id=session.id,
                    metric_type_id=metric_types[code].id,
                    value=value,
                )
            )
    if rows:
        FieldRehabMetric.objects.bulk_create(rows, ignore_conflicts=True)


def backwards(apps, schema_editor):
    FieldRehabSession = apps.get_model("main", "FieldRehabSession")
    FieldRehabMetricType = apps.get_model("main", "FieldRehabMetricType")
    FieldRehabMetric = apps.get_model("main", "FieldRehabMetric")

    code_to_field = {code: code for code, _, _ in METRIC_DEFS}
    type_map = {
        mt.id: mt.code
        for mt in FieldRehabMetricType.objects.filter(code__in=code_to_field.keys())
    }

    per_session = {}
    for metric in FieldRehabMetric.objects.filter(metric_type_id__in=type_map.keys()).iterator():
        code = type_map.get(metric.metric_type_id)
        if not code:
            continue
        per_session.setdefault(metric.session_id, {})[code] = metric.value

    for session in FieldRehabSession.objects.all().iterator():
        updates = per_session.get(session.id, {})
        changed = []
        for code, value in updates.items():
            setattr(session, code_to_field[code], value)
            changed.append(code_to_field[code])
        if changed:
            session.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0065_oefening_phase_focus_lookup_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="FieldRehabMetricType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("unit", models.CharField(blank=True, max_length=20, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="FieldRehabMetric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "metric_type",
                    models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="metric_values", to="main.fieldrehabmetrictype"),
                ),
                (
                    "session",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="metrics", to="main.fieldrehabsession"),
                ),
            ],
            options={
                "verbose_name": "Veldrevalidatie metric",
                "verbose_name_plural": "Veldrevalidatie metrics",
            },
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(model_name="fieldrehabsession", name="duur"),
        migrations.RemoveField(model_name="fieldrehabsession", name="rpe"),
        migrations.RemoveField(model_name="fieldrehabsession", name="totale_afstand"),
        migrations.RemoveField(model_name="fieldrehabsession", name="afstand_20"),
        migrations.RemoveField(model_name="fieldrehabsession", name="afstand_25"),
        migrations.RemoveField(model_name="fieldrehabsession", name="acceleraties"),
        migrations.RemoveField(model_name="fieldrehabsession", name="deceleraties"),
        migrations.AddConstraint(
            model_name="fieldrehabmetric",
            constraint=models.UniqueConstraint(fields=("session", "metric_type"), name="uniq_fieldrehab_metric_per_session"),
        ),
        migrations.AddIndex(
            model_name="fieldrehabmetric",
            index=models.Index(fields=["session", "metric_type"], name="main_fieldr_session_10d2d1_idx"),
        ),
        migrations.AddIndex(
            model_name="fieldrehabmetric",
            index=models.Index(fields=["metric_type", "value"], name="main_fieldr_metric_t_4b5748_idx"),
        ),
    ]
