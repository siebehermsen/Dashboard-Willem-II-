from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0051_backfill_birthday_youthguest_v2"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Antropometry",
        ),
    ]
