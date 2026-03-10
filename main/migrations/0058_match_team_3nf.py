import re

from django.db import migrations, models
import django.db.models.deletion


def _make_team_code(name, existing_codes):
    base = re.sub(r"[^A-Z0-9]+", "_", (name or "").upper()).strip("_")
    if not base:
        base = "TEAM"
    base = base[:20]
    code = base
    counter = 2
    while code in existing_codes:
        suffix = f"_{counter}"
        code = f"{base[: max(1, 20 - len(suffix))]}{suffix}"
        counter += 1
    existing_codes.add(code)
    return code


def forwards(apps, schema_editor):
    Team = apps.get_model("main", "Team")
    Match = apps.get_model("main", "Match")

    existing_codes = set(Team.objects.values_list("code", flat=True))
    team_by_name = {team.name: team for team in Team.objects.all()}

    def get_team(name):
        if name in team_by_name:
            return team_by_name[name]
        code = _make_team_code(name, existing_codes)
        team = Team.objects.create(name=name, code=code, is_active=True)
        team_by_name[name] = team
        return team

    for match in Match.objects.all().order_by("id"):
        home_team = get_team(getattr(match, "home", None) or "")
        away_team = get_team(getattr(match, "away", None) or "")
        match.home_team_id = home_team.id
        match.away_team_id = away_team.id
        match.save(update_fields=["home_team", "away_team"])


def backwards(apps, schema_editor):
    # Intentionally no-op. Old text columns are removed in this migration.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0057_drop_legacy_performance_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="away_team",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="away_matches",
                to="main.team",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="home_team",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="home_matches",
                to="main.team",
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveConstraint(
            model_name="match",
            name="unique_match",
        ),
        migrations.RemoveField(
            model_name="match",
            name="away",
        ),
        migrations.RemoveField(
            model_name="match",
            name="home",
        ),
        migrations.AlterField(
            model_name="match",
            name="away_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="away_matches",
                to="main.team",
            ),
        ),
        migrations.AlterField(
            model_name="match",
            name="home_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="home_matches",
                to="main.team",
            ),
        ),
        migrations.AddConstraint(
            model_name="match",
            constraint=models.UniqueConstraint(
                fields=("kickoff", "home_team", "away_team"),
                name="unique_match",
            ),
        ),
    ]
