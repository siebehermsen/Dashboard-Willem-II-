from django.db import migrations


def add_half_load_metric_types(apps, schema_editor):
    PerformanceMetricType = apps.get_model("main", "PerformanceMetricType")
    metric_defs = [
        ("first_half_load", "Load eerste helft", "au", "load"),
        ("second_half_load", "Load tweede helft", "au", "load"),
    ]
    for code, label, unit, category in metric_defs:
        PerformanceMetricType.objects.get_or_create(
            code=code,
            defaults={"label": label, "unit": unit, "category": category, "is_active": True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0095_player_is_active"),
    ]

    operations = [
        migrations.RunPython(add_half_load_metric_types, migrations.RunPython.noop),
    ]
