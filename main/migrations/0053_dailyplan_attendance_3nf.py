import datetime
from django.db import migrations, models
import django.db.models.deletion


def backfill_dailyplan_and_attendance(apps, schema_editor):
    Player = apps.get_model("main", "Player")
    DailyProgram = apps.get_model("main", "DailyProgram")
    Aanwezigheid = apps.get_model("main", "Aanwezigheid")
    IndividualDayPlan = apps.get_model("main", "IndividualDayPlan")
    IndividualDayPlanNote = apps.get_model("main", "IndividualDayPlanNote")
    AttendanceStatus = apps.get_model("main", "AttendanceStatus")
    AttendanceRecord = apps.get_model("main", "AttendanceRecord")

    status_pairs = [
        ("extern", "Extern (behandeling)"),
        ("ziek", "Ziek"),
        ("training_aangepast", "Training aangepast"),
        ("training_uitgevallen", "Training uitgevallen"),
        ("training", "Training"),
        ("wedstrijd", "Wedstrijd"),
        ("training_o21", "Training O21"),
        ("wedstrijd_o21", "Wedstrijd O21"),
        ("fysio", "Fysio"),
        ("overig", "Overig"),
    ]

    status_map = {}
    for index, (code, label) in enumerate(status_pairs, start=1):
        status, _ = AttendanceStatus.objects.get_or_create(
            code=code,
            defaults={"label": label, "sort_order": index, "is_active": True},
        )
        status_map[code] = status

    default_status = status_map["overig"]

    for player in Player.objects.all():
        for old_row in DailyProgram.objects.filter(player=player).order_by("date", "id"):
            plan, _ = IndividualDayPlan.objects.get_or_create(
                player=player,
                date=old_row.date,
            )
            note, _ = IndividualDayPlanNote.objects.get_or_create(
                plan=plan,
                note_type="program_text",
                defaults={"content": old_row.program_text or ""},
            )
            if not note.content and old_row.program_text:
                note.content = old_row.program_text
                note.save(update_fields=["content", "updated_at"])

        for old_row in Aanwezigheid.objects.filter(player=player).order_by("date", "id"):
            status = status_map.get(old_row.status, default_status)
            record, _ = AttendanceRecord.objects.get_or_create(
                player=player,
                date=old_row.date,
                defaults={"status": status, "completed": old_row.completed},
            )
            updated = False
            if record.status_id != status.id:
                record.status = status
                updated = True
            if record.completed != old_row.completed:
                record.completed = old_row.completed
                updated = True
            if updated:
                record.save(update_fields=["status", "completed", "updated_at"])


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0052_drop_legacy_antropometry"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=30, unique=True)),
                ("label", models.CharField(max_length=100)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["sort_order", "label"]},
        ),
        migrations.CreateModel(
            name="IndividualDayPlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=datetime.date.today)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("player", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="individual_day_plans", to="main.player")),
            ],
            options={"ordering": ["-date", "player__name"]},
        ),
        migrations.CreateModel(
            name="IndividualDayPlanNote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("note_type", models.CharField(default="program_text", max_length=50)),
                ("content", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("plan", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notes", to="main.individualdayplan")),
            ],
            options={"ordering": ["note_type", "id"]},
        ),
        migrations.CreateModel(
            name="AttendanceRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("player", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_records", to="main.player")),
                ("status", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="records", to="main.attendancestatus")),
            ],
            options={"ordering": ["player__name", "date"]},
        ),
        migrations.AddConstraint(
            model_name="individualdayplan",
            constraint=models.UniqueConstraint(fields=("player", "date"), name="uniq_individual_day_plan_player_date"),
        ),
        migrations.AddConstraint(
            model_name="individualdayplannote",
            constraint=models.UniqueConstraint(fields=("plan", "note_type"), name="uniq_individual_day_plan_note_type"),
        ),
        migrations.AddConstraint(
            model_name="attendancerecord",
            constraint=models.UniqueConstraint(fields=("player", "date"), name="uniq_attendance_player_date"),
        ),
        migrations.AddIndex(
            model_name="attendancerecord",
            index=models.Index(fields=["date", "status"], name="main_attend_date_1efd36_idx"),
        ),
        migrations.RunPython(backfill_dailyplan_and_attendance, migrations.RunPython.noop),
    ]
