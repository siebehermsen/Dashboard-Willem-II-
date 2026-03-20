from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0090_trainingweektarget"),
    ]

    operations = [
        migrations.CreateModel(
            name="BeleidSectionImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("page_key", models.CharField(default="beleid", max_length=50)),
                ("section_key", models.CharField(max_length=50)),
                ("image", models.ImageField(upload_to="beleid_images/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at", "-id"],
            },
        ),
        migrations.AddIndex(
            model_name="beleidsectionimage",
            index=models.Index(fields=["page_key", "section_key"], name="main_beleid_page_se_65fb58_idx"),
        ),
    ]
