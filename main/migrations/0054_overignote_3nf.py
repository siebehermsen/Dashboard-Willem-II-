import re
from django.db import migrations, models


PREFIX_RE = re.compile(r"^\[(?P<page>[a-z0-9\-_]+):(?P<section>[a-z0-9\-_]+)\](?P<text>.*)$", re.IGNORECASE | re.DOTALL)


def backfill_overig_to_overignote(apps, schema_editor):
    Overig = apps.get_model("main", "Overig")
    OverigNote = apps.get_model("main", "OverigNote")

    for row in Overig.objects.all().order_by("created_at", "id"):
        raw = (row.text or "").strip()
        if not raw:
            continue

        match = PREFIX_RE.match(raw)
        if match:
            OverigNote.objects.create(
                note_type="section",
                page_key=match.group("page").strip().lower(),
                section_key=match.group("section").strip().lower(),
                text=(match.group("text") or "").strip(),
            )
        else:
            OverigNote.objects.create(
                note_type="note",
                page_key="notities",
                section_key=None,
                text=raw,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0053_dailyplan_attendance_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="OverigNote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("note_type", models.CharField(choices=[("note", "Vrije notitie"), ("section", "Sectietekst")], default="note", max_length=20)),
                ("page_key", models.CharField(blank=True, max_length=50, null=True)),
                ("section_key", models.CharField(blank=True, max_length=50, null=True)),
                ("text", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.AddIndex(
            model_name="overignote",
            index=models.Index(fields=["note_type", "page_key", "section_key"], name="main_overign_note_ty_5f60f5_idx"),
        ),
        migrations.AddIndex(
            model_name="overignote",
            index=models.Index(fields=["created_at"], name="main_overign_created_32941d_idx"),
        ),
        migrations.RunPython(backfill_overig_to_overignote, migrations.RunPython.noop),
    ]
