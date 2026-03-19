from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0086_alter_rpeentry_rpe_alter_wellnessentry_fitness_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="programma",
            name="plan_komende_periode",
            field=models.TextField(blank=True, null=True, verbose_name="Plan komende periode"),
        ),
        migrations.AddField(
            model_name="programma",
            name="sterke_punten",
            field=models.TextField(blank=True, null=True, verbose_name="Sterke punten"),
        ),
        migrations.AddField(
            model_name="programma",
            name="verbeterpunten",
            field=models.TextField(blank=True, null=True, verbose_name="Verbeterpunten"),
        ),
    ]
