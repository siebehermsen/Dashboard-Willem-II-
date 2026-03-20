from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0092_staff_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="image",
            field=models.FileField(blank=True, null=True, upload_to="staff_images/"),
        ),
    ]
