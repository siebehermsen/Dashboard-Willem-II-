from django.db import migrations


def forwards(apps, schema_editor):
    # Intentional no-op.
    # This migration marks the point where legacy tables are no longer used
    # by primary read/write paths in the application code.
    pass


def backwards(apps, schema_editor):
    # No-op rollback marker.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0048_merge_0046_rename_and_0047_nutrition"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

