from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    Player = apps.get_model("main", "Player")
    Staff = apps.get_model("main", "Staff")
    PlayerPosition = apps.get_model("main", "PlayerPosition")
    StaffRole = apps.get_model("main", "StaffRole")

    position_cache = {}
    role_cache = {}

    # Seed known player positions from legacy choices if absent.
    known_positions = [
        "Spits",
        "Targetman",
        "Buitenspeler",
        "Dynamische middenvelder",
        "Controlerende middenvelder",
        "Centrale verdediger",
        "Vleugelverdediger",
    ]
    for name in known_positions:
        obj, _ = PlayerPosition.objects.get_or_create(name=name, defaults={"is_active": True})
        position_cache[name] = obj

    for player in Player.objects.all().order_by("id"):
        value = (getattr(player, "position", None) or "").strip()
        if not value:
            continue
        obj = position_cache.get(value)
        if obj is None:
            obj, _ = PlayerPosition.objects.get_or_create(name=value, defaults={"is_active": True})
            position_cache[value] = obj
        player.position_ref_id = obj.id
        player.save(update_fields=["position_ref"])

    for staff in Staff.objects.all().order_by("id"):
        value = (getattr(staff, "role", None) or "").strip()
        if not value:
            continue
        obj = role_cache.get(value)
        if obj is None:
            obj, _ = StaffRole.objects.get_or_create(name=value, defaults={"is_active": True})
            role_cache[value] = obj
        staff.role_ref_id = obj.id
        staff.save(update_fields=["role_ref"])


def backwards(apps, schema_editor):
    # No-op: legacy text fields are removed in this migration.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0063_player_monitoring_profile_3nf"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerPosition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="StaffRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="player",
            name="position_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="players",
                to="main.playerposition",
                verbose_name="Positie",
            ),
        ),
        migrations.AddField(
            model_name="staff",
            name="role_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="staff_members",
                to="main.staffrole",
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(model_name="player", name="position"),
        migrations.RemoveField(model_name="staff", name="role"),
    ]
