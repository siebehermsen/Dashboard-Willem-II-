from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0038_vakantieplanning"),
    ]

    operations = [
        migrations.CreateModel(
            name="GrowthProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("age", models.FloatField(blank=True, null=True, verbose_name="Leeftijd (jaren)")),
                ("height", models.FloatField(blank=True, null=True, verbose_name="Lengte (cm)")),
                ("sitting_height", models.FloatField(blank=True, null=True, verbose_name="Zithoogte (cm)")),
                ("weight", models.FloatField(blank=True, null=True, verbose_name="Gewicht (kg)")),
                ("maturity_offset", models.FloatField(blank=True, null=True, verbose_name="Maturity offset")),
                ("growth_complaints", models.BooleanField(default=False, verbose_name="Groeiklachten")),
                ("action", models.CharField(blank=True, max_length=255, null=True, verbose_name="Actie")),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("player", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="growth_profile", to="main.player")),
            ],
            options={
                "verbose_name": "Groeiprofiel",
                "verbose_name_plural": "Groeiprofielen",
                "ordering": ["player__name"],
            },
        ),
        migrations.CreateModel(
            name="GrowthMeasurement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Meetdatum")),
                ("height_cm", models.FloatField(verbose_name="Lengte (cm)")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="measurements", to="main.growthprofile")),
            ],
            options={
                "verbose_name": "Groeimeetpunt",
                "verbose_name_plural": "Groeimeetpunten",
                "ordering": ["date", "id"],
                "unique_together": {("profile", "date")},
            },
        ),
    ]
