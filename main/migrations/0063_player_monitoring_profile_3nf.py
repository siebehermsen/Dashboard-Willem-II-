from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    Player = apps.get_model("main", "Player")
    PlayerMonitoringProfile = apps.get_model("main", "PlayerMonitoringProfile")

    for player in Player.objects.all().order_by("id"):
        has_data = any(
            value not in (None, "")
            for value in [
                getattr(player, "prev_weight", None),
                getattr(player, "curr_weight", None),
                getattr(player, "sum_skinfolds", None),
                getattr(player, "fat_perc", None),
                getattr(player, "nutrition_focus", None),
            ]
        )
        if not has_data:
            continue

        PlayerMonitoringProfile.objects.update_or_create(
            player_id=player.id,
            defaults={
                "prev_weight": getattr(player, "prev_weight", None),
                "curr_weight": getattr(player, "curr_weight", None),
                "sum_skinfolds": getattr(player, "sum_skinfolds", None),
                "fat_perc": getattr(player, "fat_perc", None),
                "nutrition_focus": getattr(player, "nutrition_focus", None),
            },
        )


def backwards(apps, schema_editor):
    # No-op: legacy fields are removed from Player in this migration.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0062_rpe_training_type_lookup_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerMonitoringProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("prev_weight", models.FloatField(blank=True, null=True, verbose_name="Vorig gewicht (kg)")),
                ("curr_weight", models.FloatField(blank=True, null=True, verbose_name="Huidig gewicht (kg)")),
                ("sum_skinfolds", models.FloatField(blank=True, null=True, verbose_name="Som huidplooien (mm)")),
                ("fat_perc", models.FloatField(blank=True, null=True, verbose_name="Vetpercentage (%)")),
                (
                    "nutrition_focus",
                    models.TextField(
                        blank=True,
                        help_text="Bijv. 'Meer ontbijt eten', 'Extra herstelshake nemen na training', etc.",
                        null=True,
                        verbose_name="Voedingsaandachtspunt",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="monitoring_profile",
                        to="main.player",
                    ),
                ),
            ],
            options={"ordering": ["player__name"]},
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(model_name="player", name="curr_weight"),
        migrations.RemoveField(model_name="player", name="fat_perc"),
        migrations.RemoveField(model_name="player", name="nutrition_focus"),
        migrations.RemoveField(model_name="player", name="prev_weight"),
        migrations.RemoveField(model_name="player", name="sum_skinfolds"),
    ]
