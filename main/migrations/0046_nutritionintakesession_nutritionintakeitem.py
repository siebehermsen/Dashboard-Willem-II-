from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0045_backfill_anthropometry_v2"),
    ]

    operations = [
        migrations.CreateModel(
            name="NutritionIntakeSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(blank=True, null=True)),
                ("goal", models.CharField(blank=True, max_length=255, null=True)),
                ("next_meeting_goal", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nutrition_sessions",
                        to="main.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-date", "-updated_at", "-id"],
                "indexes": [models.Index(fields=["player", "date"], name="main_nutrit_player__b53571_idx")],
            },
        ),
        migrations.CreateModel(
            name="NutritionIntakeItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "meal_key",
                    models.CharField(
                        choices=[
                            ("breakfast", "Ontbijt"),
                            ("snack1", "Snack 1"),
                            ("lunch", "Lunch"),
                            ("snack2", "Snack 2"),
                            ("dinner", "Diner"),
                            ("snack3", "Snack 3"),
                            ("supplements", "Supplementen"),
                        ],
                        max_length=30,
                    ),
                ),
                ("value", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="main.nutritionintakesession",
                    ),
                ),
            ],
            options={
                "ordering": ["meal_key"],
                "constraints": [
                    models.UniqueConstraint(fields=("session", "meal_key"), name="uniq_nutrition_item_per_meal")
                ],
            },
        ),
    ]

