from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0056_performance_session_metric_3nf"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL("DROP TABLE IF EXISTS main_trainingdata"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_wedstrijddata"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_playertest"),
            ],
            state_operations=[
                migrations.DeleteModel(name="TrainingData"),
                migrations.DeleteModel(name="WedstrijdData"),
                migrations.DeleteModel(name="PlayerTest"),
            ],
        ),
    ]
