from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0088_programma_video_links"),
    ]

    operations = [
        migrations.AddField(
            model_name="programma",
            name="evaluatie_datum",
            field=models.DateField(blank=True, null=True, verbose_name="Evaluatiedatum"),
        ),
        migrations.AddField(
            model_name="programma",
            name="fysiek_ontwikkelpunt",
            field=models.TextField(blank=True, null=True, verbose_name="Fysiek ontwikkelpunt"),
        ),
        migrations.AddField(
            model_name="programma",
            name="ontwikkelaanpak",
            field=models.TextField(blank=True, null=True, verbose_name="Hoe gaat de speler dit ontwikkelen"),
        ),
    ]
