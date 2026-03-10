from django.db import migrations


def forwards(apps, schema_editor):
    PlayerIntake = apps.get_model("main", "PlayerIntake")
    NutritionIntakeSession = apps.get_model("main", "NutritionIntakeSession")
    NutritionIntakeItem = apps.get_model("main", "NutritionIntakeItem")

    meal_keys = ["breakfast", "snack1", "lunch", "snack2", "dinner", "snack3", "supplements"]

    for legacy in PlayerIntake.objects.all().order_by("id"):
        session = NutritionIntakeSession.objects.create(
            player=legacy.player,
            date=legacy.date,
            goal=legacy.goal,
            next_meeting_goal=legacy.next_meeting_goal,
        )
        for key in meal_keys:
            NutritionIntakeItem.objects.create(
                session=session,
                meal_key=key,
                value=getattr(legacy, key, "") or "",
            )


def backwards(apps, schema_editor):
    # No-op: v2 historie niet terugschrijven naar legacy one-to-one record.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0046_nutritionintakesession_nutritionintakeitem"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

