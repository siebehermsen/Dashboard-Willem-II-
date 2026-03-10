from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0049_deprecate_legacy_tables_preflight"),
    ]

    operations = [
        migrations.CreateModel(
            name="BirthdayProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                (
                    "role",
                    models.CharField(
                        blank=True,
                        choices=[("Speler", "Speler"), ("Staf", "Staf"), ("Overig", "Overig")],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["name"],
                "constraints": [
                    models.UniqueConstraint(fields=("name", "role"), name="uniq_birthday_profile_name_role")
                ],
            },
        ),
        migrations.CreateModel(
            name="YouthGuestProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("team", models.CharField(blank=True, max_length=100, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["name"],
                "constraints": [
                    models.UniqueConstraint(fields=("name", "team"), name="uniq_youthguest_profile_name_team")
                ],
            },
        ),
        migrations.CreateModel(
            name="BirthdayRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="main.birthdayprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["date", "profile__name"],
                "constraints": [
                    models.UniqueConstraint(fields=("profile", "date"), name="uniq_birthday_profile_date")
                ],
            },
        ),
        migrations.CreateModel(
            name="YouthGuestWeek",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("week_of", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weeks",
                        to="main.youthguestprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["-week_of", "profile__name"],
                "constraints": [
                    models.UniqueConstraint(fields=("profile", "week_of"), name="uniq_youthguest_profile_week")
                ],
            },
        ),
    ]

