from decimal import Decimal, InvalidOperation
import re

from django.db import migrations, models


def parse_duur(value):
    if value in (None, ""):
        return None, None, None
    text = str(value).strip()
    if not text:
        return None, None, None
    match = re.match(r"^\s*([0-9]+(?:[.,][0-9]+)?)\s*(.*)\s*$", text)
    if not match:
        return None, None, text
    number_raw = match.group(1).replace(",", ".")
    unit_raw = (match.group(2) or "").strip() or None
    try:
        parsed = Decimal(number_raw)
    except (InvalidOperation, ValueError):
        return None, None, text
    return parsed, unit_raw, None


def forwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    ProgrammaDuurUnit = apps.get_model("main", "ProgrammaDuurUnit")

    unit_cache = {}
    for oef in ProgrammaOefening.objects.all().iterator():
        raw = getattr(oef, "duur", None)
        value, unit_name, override = parse_duur(raw)
        oef.duur_value = value
        oef.duur_text_override = override
        if unit_name:
            if unit_name not in unit_cache:
                unit_cache[unit_name], _ = ProgrammaDuurUnit.objects.get_or_create(name=unit_name)
            oef.duur_unit_ref_id = unit_cache[unit_name].id
        else:
            oef.duur_unit_ref_id = None
        oef.save(update_fields=["duur_value", "duur_unit_ref", "duur_text_override"])


def backwards(apps, schema_editor):
    ProgrammaOefening = apps.get_model("main", "ProgrammaOefening")
    for oef in ProgrammaOefening.objects.select_related("duur_unit_ref").all().iterator():
        if oef.duur_text_override:
            text = oef.duur_text_override
        elif oef.duur_value is None:
            text = None
        else:
            value = oef.duur_value
            if value == value.to_integral_value():
                value_str = str(int(value))
            else:
                value_str = format(value.normalize(), "f").rstrip("0").rstrip(".")
            text = value_str if not oef.duur_unit_ref_id else f"{value_str} {oef.duur_unit_ref.name}"
        oef.duur = text
        oef.save(update_fields=["duur"])


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0068_programma_oefening_rpe_numeric_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgrammaDuurUnit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="programmaoefening",
            name="duur_text_override",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="programmaoefening",
            name="duur_unit_ref",
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name="oefeningen", to="main.programmaduurunit"),
        ),
        migrations.AddField(
            model_name="programmaoefening",
            name="duur_value",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="programmaoefening",
            name="duur",
        ),
        migrations.AddIndex(
            model_name="programmaoefening",
            index=models.Index(fields=["duur_unit_ref"], name="main_progra_duur_un_9db8f4_idx"),
        ),
        migrations.AddIndex(
            model_name="programmaoefening",
            index=models.Index(fields=["duur_value"], name="main_progra_duur_va_237147_idx"),
        ),
    ]
