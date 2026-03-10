from django.db import migrations, models


def forwards(apps, schema_editor):
    YouthGuestProfile = apps.get_model("main", "YouthGuestProfile")
    YouthGuestTeam = apps.get_model("main", "YouthGuestTeam")

    cache = {}
    for profile in YouthGuestProfile.objects.all().iterator():
        raw = getattr(profile, "team", None)
        if raw is None:
            continue
        text = str(raw).strip()
        if not text:
            continue
        if text not in cache:
            cache[text], _ = YouthGuestTeam.objects.get_or_create(name=text)
        profile.team_ref_id = cache[text].id
        profile.save(update_fields=["team_ref"])


def backwards(apps, schema_editor):
    YouthGuestProfile = apps.get_model("main", "YouthGuestProfile")
    for profile in YouthGuestProfile.objects.select_related("team_ref").all().iterator():
        if profile.team_ref_id:
            profile.team = profile.team_ref.name
            profile.save(update_fields=["team"])


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0072_hit_asr_planning_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="YouthGuestTeam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="youthguestprofile",
            name="team_ref",
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name="profiles", to="main.youthguestteam"),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveConstraint(
            model_name="youthguestprofile",
            name="uniq_youthguest_profile_name_team",
        ),
        migrations.RemoveField(
            model_name="youthguestprofile",
            name="team",
        ),
        migrations.AddConstraint(
            model_name="youthguestprofile",
            constraint=models.UniqueConstraint(fields=("name", "team_ref"), name="uniq_youthguest_profile_name_team_ref"),
        ),
        migrations.AddIndex(
            model_name="youthguestprofile",
            index=models.Index(fields=["team_ref"], name="main_youthg_team_re_8fceab_idx"),
        ),
    ]
