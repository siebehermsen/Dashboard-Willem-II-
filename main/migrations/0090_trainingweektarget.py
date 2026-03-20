from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0089_programma_fysiek_ontwikkelpunt"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrainingWeekTarget",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Geplande weektargets training", max_length=120)),
                ("monday", models.CharField(blank=True, default="", max_length=255, verbose_name="Maandag")),
                ("tuesday", models.CharField(blank=True, default="", max_length=255, verbose_name="Dinsdag")),
                ("wednesday", models.CharField(blank=True, default="", max_length=255, verbose_name="Woensdag")),
                ("thursday", models.CharField(blank=True, default="", max_length=255, verbose_name="Donderdag")),
                ("friday", models.CharField(blank=True, default="", max_length=255, verbose_name="Vrijdag")),
                ("saturday", models.CharField(blank=True, default="", max_length=255, verbose_name="Zaterdag")),
                ("sunday", models.CharField(blank=True, default="", max_length=255, verbose_name="Zondag")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Training weektarget",
                "verbose_name_plural": "Training weektargets",
                "ordering": ["-updated_at"],
            },
        ),
    ]
