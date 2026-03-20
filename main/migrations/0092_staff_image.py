from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0091_beleidsectionimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="staff_images/"),
        ),
    ]
