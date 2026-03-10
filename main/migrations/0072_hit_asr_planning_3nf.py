from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0071_player_speed_test_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="HitAsrPlanSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_date", models.DateField()),
                ("mas_percent", models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Intensiteit (%MAS)")),
                ("reference_speed_kmh", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ("notes", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "HIT ASR planning",
                "verbose_name_plural": "HIT ASR planningen",
                "ordering": ["-session_date", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="HitAsrPlanEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mss_kmh", models.DecimalField(decimal_places=2, max_digits=5)),
                ("mas_kmh", models.DecimalField(decimal_places=2, max_digits=5)),
                ("target_speed_kmh", models.DecimalField(decimal_places=2, max_digits=6)),
                ("asr_kmh", models.DecimalField(decimal_places=2, max_digits=5)),
                ("pct_mas", models.DecimalField(decimal_places=2, max_digits=6)),
                ("pct_asr", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ("indication", models.CharField(blank=True, max_length=40, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("player", models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="hit_asr_plan_entries", to="main.player")),
                ("session", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="entries", to="main.hitasrplansession")),
            ],
            options={
                "verbose_name": "HIT ASR planning regel",
                "verbose_name_plural": "HIT ASR planning regels",
                "ordering": ["player__name"],
            },
        ),
        migrations.AddConstraint(
            model_name="hitasrplanentry",
            constraint=models.UniqueConstraint(fields=("session", "player"), name="uniq_hit_asr_plan_session_player"),
        ),
        migrations.AddIndex(
            model_name="hitasrplansession",
            index=models.Index(fields=["session_date"], name="main_hitasr_session_494a1c_idx"),
        ),
        migrations.AddIndex(
            model_name="hitasrplansession",
            index=models.Index(fields=["created_at"], name="main_hitasr_created_f77e65_idx"),
        ),
        migrations.AddIndex(
            model_name="hitasrplanentry",
            index=models.Index(fields=["session", "player"], name="main_hitasr_session_e57696_idx"),
        ),
        migrations.AddIndex(
            model_name="hitasrplanentry",
            index=models.Index(fields=["player", "created_at"], name="main_hitasr_player__384ed0_idx"),
        ),
    ]
