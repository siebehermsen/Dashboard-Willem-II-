from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0096_half_load_metric_types"),
    ]

    operations = [
        migrations.CreateModel(
            name="MDOActionPoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("owner", models.CharField(blank=True, default="", max_length=120)),
                ("deadline", models.DateField(blank=True, null=True)),
                (
                    "status_color",
                    models.CharField(
                        choices=[("green", "Groen"), ("orange", "Oranje"), ("red", "Rood")],
                        default="orange",
                        max_length=20,
                    ),
                ),
                ("is_done", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mdo_action_points",
                        to="main.player",
                    ),
                ),
            ],
            options={
                "ordering": ["is_done", "deadline", "-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="mdoactionpoint",
            index=models.Index(fields=["player", "is_done", "deadline"], name="main_mdo_player_done_dead_idx"),
        ),
        migrations.AddIndex(
            model_name="mdoactionpoint",
            index=models.Index(fields=["status_color"], name="main_mdo_status_color_idx"),
        ),
    ]
