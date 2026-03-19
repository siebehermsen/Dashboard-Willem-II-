from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0087_programma_beeldenvelden"),
    ]

    operations = [
        migrations.AddField(
            model_name="programma",
            name="video_links",
            field=models.TextField(blank=True, null=True, verbose_name="Videolinks"),
        ),
    ]
