from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0043_backfill_dayprogramentry"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnthropometrySession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("body_mass", models.FloatField(blank=True, null=True)),
                ("length", models.FloatField(blank=True, null=True)),
                ("fat_dw", models.FloatField(blank=True, null=True)),
                ("fat_faulkner", models.FloatField(blank=True, null=True)),
                ("fat_carter", models.FloatField(blank=True, null=True)),
                ("fat_average", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="anthropometry_sessions",
                        to="main.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-date", "-id"],
                "constraints": [
                    models.UniqueConstraint(fields=("player", "date"), name="uniq_anthro_session_player_date")
                ],
            },
        ),
        migrations.CreateModel(
            name="AnthropometryMeasurement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "category",
                    models.CharField(choices=[("skinfold", "Skinfold"), ("girth", "Girth")], max_length=20),
                ),
                ("site_code", models.CharField(max_length=50)),
                ("repetition", models.PositiveSmallIntegerField()),
                ("value", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="measurements",
                        to="main.anthropometrysession",
                    ),
                ),
            ],
            options={
                "ordering": ["category", "site_code", "repetition"],
                "indexes": [models.Index(fields=["category", "site_code"], name="main_anthro_category_3366cb_idx")],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("session", "category", "site_code", "repetition"),
                        name="uniq_anthro_measurement_per_rep",
                    )
                ],
            },
        ),
    ]

