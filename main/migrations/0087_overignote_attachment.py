from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0086_alter_rpeentry_rpe_alter_wellnessentry_fitness_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="overignote",
            name="attachment",
            field=models.FileField(blank=True, null=True, upload_to="beleid_uploads/"),
        ),
    ]
