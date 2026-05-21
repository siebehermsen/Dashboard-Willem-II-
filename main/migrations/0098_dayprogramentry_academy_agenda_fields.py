from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0097_mdoactionpoint"),
    ]

    operations = [
        migrations.AddField(
            model_name="dayprogramentry",
            name="category",
            field=models.CharField(blank=True, default="training", max_length=40),
        ),
        migrations.AddField(
            model_name="dayprogramentry",
            name="context",
            field=models.CharField(blank=True, default="", max_length=120),
        ),
        migrations.AddField(
            model_name="dayprogramentry",
            name="end_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="dayprogramentry",
            name="location",
            field=models.CharField(blank=True, default="", max_length=120),
        ),
        migrations.AddField(
            model_name="dayprogramentry",
            name="physical_note",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="dayprogramentry",
            name="responsible",
            field=models.CharField(blank=True, default="", max_length=120),
        ),
        migrations.AddField(
            model_name="dayprogramentry",
            name="start_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="dayprogramentry",
            name="team",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
    ]
