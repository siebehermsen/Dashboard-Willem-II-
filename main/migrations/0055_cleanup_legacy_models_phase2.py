from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0054_overignote_3nf"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL("DROP TABLE IF EXISTS main_birthday"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_youthguest"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_injury"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_dayprogram"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_overig"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_hitweekplanning"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_dailyprogram"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_aanwezigheid"),
                migrations.RunSQL("DROP TABLE IF EXISTS main_playerintake"),
            ],
            state_operations=[
                migrations.DeleteModel(name="Birthday"),
                migrations.DeleteModel(name="YouthGuest"),
                migrations.DeleteModel(name="Injury"),
                migrations.DeleteModel(name="DayProgram"),
                migrations.DeleteModel(name="Overig"),
                migrations.DeleteModel(name="HitWeekPlanning"),
                migrations.DeleteModel(name="DailyProgram"),
                migrations.DeleteModel(name="Aanwezigheid"),
                migrations.DeleteModel(name="PlayerIntake"),
            ],
        ),
    ]
