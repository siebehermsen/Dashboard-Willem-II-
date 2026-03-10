from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0039_growthprofile_growthmeasurement"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="DayProgramEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("title", models.CharField(blank=True, max_length=120, null=True)),
                ("activities", models.TextField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["date", "id"],
                "constraints": [
                    models.UniqueConstraint(fields=("date", "title"), name="uniq_dayprogram_date_title")
                ],
            },
        ),
        migrations.CreateModel(
            name="HitWeekPlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Algemene HIT Weekplanning", max_length=120)),
                ("week_start", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "trainer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="hit_week_plans",
                        to="auth.user",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="InjuryCase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("injury_type", models.CharField(max_length=100)),
                ("phase", models.CharField(blank=True, max_length=50, null=True)),
                ("status", models.CharField(default="active", max_length=30)),
                ("started_on", models.DateField(blank=True, null=True)),
                ("expected_return_on", models.DateField(blank=True, null=True)),
                ("closed_on", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="injury_cases",
                        to="main.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["player", "status"], name="main_injuryc_player__8c0f5b_idx"),
                    models.Index(fields=["started_on"], name="main_injuryc_started_34f452_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="PlayerTeamAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_assignments",
                        to="main.player",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="player_assignments",
                        to="main.team",
                    ),
                ),
            ],
            options={
                "ordering": ["-start_date", "player__name"],
                "constraints": [
                    models.UniqueConstraint(fields=("player", "team", "start_date"), name="uniq_player_team_start")
                ],
            },
        ),
        migrations.CreateModel(
            name="HitWeekPlanEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "day_of_week",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Maandag"),
                            (2, "Dinsdag"),
                            (3, "Woensdag"),
                            (4, "Donderdag"),
                            (5, "Vrijdag"),
                            (6, "Zaterdag"),
                            (7, "Zondag"),
                        ]
                    ),
                ),
                ("content", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="main.hitweekplan",
                    ),
                ),
            ],
            options={
                "ordering": ["day_of_week"],
                "constraints": [
                    models.UniqueConstraint(fields=("plan", "day_of_week"), name="uniq_hitplan_day")
                ],
            },
        ),
    ]

