from django.db import migrations


def forwards(apps, schema_editor):
    Birthday = apps.get_model("main", "Birthday")
    BirthdayProfile = apps.get_model("main", "BirthdayProfile")
    BirthdayRecord = apps.get_model("main", "BirthdayRecord")

    YouthGuest = apps.get_model("main", "YouthGuest")
    YouthGuestProfile = apps.get_model("main", "YouthGuestProfile")
    YouthGuestWeek = apps.get_model("main", "YouthGuestWeek")

    for legacy in Birthday.objects.all().order_by("id"):
        profile, _ = BirthdayProfile.objects.get_or_create(
            name=legacy.name,
            role=legacy.role,
        )
        BirthdayRecord.objects.get_or_create(
            profile=profile,
            date=legacy.date,
        )

    for legacy in YouthGuest.objects.all().order_by("id"):
        profile, _ = YouthGuestProfile.objects.get_or_create(
            name=legacy.name,
            team=legacy.team,
        )
        YouthGuestWeek.objects.get_or_create(
            profile=profile,
            week_of=legacy.week_of,
        )


def backwards(apps, schema_editor):
    # No-op: do not remove v2 records automatically.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0050_birthdayprofile_birthdayrecord_youthguestprofile_youthguestweek"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

