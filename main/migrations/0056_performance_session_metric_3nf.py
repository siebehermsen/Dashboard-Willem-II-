from django.db import migrations, models
import django.db.models.deletion


def backfill_performance_3nf(apps, schema_editor):
    TrainingData = apps.get_model("main", "TrainingData")
    WedstrijdData = apps.get_model("main", "WedstrijdData")
    PlayerTest = apps.get_model("main", "PlayerTest")
    PerformanceSession = apps.get_model("main", "PerformanceSession")
    PerformanceMetricType = apps.get_model("main", "PerformanceMetricType")
    PerformanceMetric = apps.get_model("main", "PerformanceMetric")

    metric_defs = [
        ("total_distance", "Totale afstand", "m", "load"),
        ("hsd", "High-speed distance", "m", "load"),
        ("sprints", "Sprints", "count", "load"),
        ("load", "Belasting", "au", "load"),
        ("accelerations", "Acceleraties", "count", "load"),
        ("decelerations", "Deceleraties", "count", "load"),
        ("his", "High intensity sprint distance", "m", "load"),
        ("sprint_10", "10m sprint", "s", "test"),
        ("sprint_30", "30m sprint", "s", "test"),
        ("cmj", "CMJ", "cm", "test"),
        ("squat_jump", "Squat jump", "cm", "test"),
        ("isrt", "ISRT", "m", "test"),
        ("submax", "Submax", "pct", "test"),
        ("curr_weight", "Gewicht", "kg", "test"),
        ("length", "Lengte", "cm", "test"),
        ("sum_skinfolds", "Som huidplooien", "mm", "test"),
    ]

    metric_types = {}
    for code, label, unit, category in metric_defs:
        obj, _ = PerformanceMetricType.objects.get_or_create(
            code=code,
            defaults={"label": label, "unit": unit, "category": category, "is_active": True},
        )
        metric_types[code] = obj

    def upsert_metric(session, code, raw):
        if raw is None or raw == "":
            return
        try:
            val = float(raw)
        except (TypeError, ValueError):
            return
        metric_type = metric_types[code]
        PerformanceMetric.objects.update_or_create(
            session=session,
            metric_type=metric_type,
            defaults={"value": val},
        )

    for row in TrainingData.objects.all().order_by("id"):
        session, _ = PerformanceSession.objects.get_or_create(
            player_id=row.player_id,
            session_kind="training",
            session_date=row.session_date,
            source_legacy_table="main_trainingdata",
            source_legacy_id=row.id,
            defaults={"week": row.week},
        )
        if session.week != row.week:
            session.week = row.week
            session.save(update_fields=["week", "updated_at"])
        upsert_metric(session, "total_distance", row.total_distance)
        upsert_metric(session, "hsd", row.hsd)
        upsert_metric(session, "sprints", row.sprints)
        upsert_metric(session, "load", row.load)

    for row in WedstrijdData.objects.all().order_by("id"):
        session, _ = PerformanceSession.objects.get_or_create(
            player_id=row.player_id,
            session_kind="match",
            session_date=row.match_date,
            source_legacy_table="main_wedstrijddata",
            source_legacy_id=row.id,
            defaults={"week": row.week},
        )
        if session.week != row.week:
            session.week = row.week
            session.save(update_fields=["week", "updated_at"])
        upsert_metric(session, "accelerations", row.accelerations)
        upsert_metric(session, "decelerations", row.decelerations)
        upsert_metric(session, "hsd", row.hsd)
        upsert_metric(session, "his", row.his)
        upsert_metric(session, "total_distance", row.total_distance)
        upsert_metric(session, "sprints", row.sprints)
        upsert_metric(session, "load", row.load)

    for row in PlayerTest.objects.all().order_by("id"):
        session, _ = PerformanceSession.objects.get_or_create(
            player_id=row.player_id,
            session_kind="test",
            session_date=row.test_date,
            source_legacy_table="main_playertest",
            source_legacy_id=row.id,
            defaults={"week": None},
        )
        upsert_metric(session, "sprint_10", row.sprint_10)
        upsert_metric(session, "sprint_30", row.sprint_30)
        upsert_metric(session, "cmj", row.cmj)
        upsert_metric(session, "squat_jump", row.squat_jump)
        upsert_metric(session, "isrt", row.isrt)
        upsert_metric(session, "submax", row.submax)
        upsert_metric(session, "curr_weight", row.curr_weight)
        upsert_metric(session, "length", row.length)
        upsert_metric(session, "sum_skinfolds", row.sum_skinfolds)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0055_cleanup_legacy_models_phase2"),
    ]

    operations = [
        migrations.CreateModel(
            name="PerformanceMetricType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=50, unique=True)),
                ("label", models.CharField(max_length=120)),
                ("unit", models.CharField(blank=True, default="", max_length=30)),
                ("category", models.CharField(blank=True, default="", max_length=30)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["category", "label"]},
        ),
        migrations.CreateModel(
            name="PerformanceSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_kind", models.CharField(choices=[("training", "Training"), ("match", "Wedstrijd"), ("test", "Test")], max_length=20)),
                ("session_date", models.DateField()),
                ("week", models.PositiveIntegerField(blank=True, null=True)),
                ("source_legacy_table", models.CharField(blank=True, max_length=50, null=True)),
                ("source_legacy_id", models.PositiveIntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("player", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="performance_sessions", to="main.player")),
            ],
            options={"ordering": ["-session_date", "player__name", "session_kind"]},
        ),
        migrations.CreateModel(
            name="PerformanceMetric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("metric_type", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="values", to="main.performancemetrictype")),
                ("session", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="metrics", to="main.performancesession")),
            ],
            options={"ordering": ["session_id", "metric_type__code"]},
        ),
        migrations.AddConstraint(
            model_name="performancesession",
            constraint=models.UniqueConstraint(fields=("player", "session_kind", "session_date", "source_legacy_table", "source_legacy_id"), name="uniq_perf_session_per_source"),
        ),
        migrations.AddIndex(
            model_name="performancesession",
            index=models.Index(fields=["session_kind", "session_date"], name="main_perfor_session_8134f5_idx"),
        ),
        migrations.AddIndex(
            model_name="performancesession",
            index=models.Index(fields=["player", "session_date"], name="main_perfor_player__1b5325_idx"),
        ),
        migrations.AddConstraint(
            model_name="performancemetric",
            constraint=models.UniqueConstraint(fields=("session", "metric_type"), name="uniq_perf_metric_per_session_type"),
        ),
        migrations.AddIndex(
            model_name="performancemetric",
            index=models.Index(fields=["metric_type", "value"], name="main_perfor_metric__55685d_idx"),
        ),
        migrations.RunPython(backfill_performance_3nf, migrations.RunPython.noop),
    ]
