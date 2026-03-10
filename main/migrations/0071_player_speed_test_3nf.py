from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0070_programma_oefening_name_lookup_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerSpeedTest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("test_date", models.DateField()),
                ("mss_kmh", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="MSS (km/u)")),
                ("mas_kmh", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="MAS (km/u)")),
                ("notes", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="speed_tests", to="main.player"),
                ),
            ],
            options={
                "verbose_name": "Snelheidstest (MSS/MAS)",
                "verbose_name_plural": "Snelheidstesten (MSS/MAS)",
                "ordering": ["-test_date", "player__name"],
            },
        ),
        migrations.AddConstraint(
            model_name="playerspeedtest",
            constraint=models.UniqueConstraint(fields=("player", "test_date"), name="uniq_speed_test_player_date"),
        ),
        migrations.AddIndex(
            model_name="playerspeedtest",
            index=models.Index(fields=["player", "test_date"], name="main_players_player__2f9317_idx"),
        ),
        migrations.AddIndex(
            model_name="playerspeedtest",
            index=models.Index(fields=["test_date"], name="main_players_test_da_2efea4_idx"),
        ),
    ]
