from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import (
    AttendanceRecord,
    AttendanceStatus,
    DayProgramEntry,
    MDOActionPoint,
    NutritionIntakeItem,
    NutritionIntakeSession,
    OverigNote,
    PerformanceMetric,
    PerformanceMetricType,
    PerformanceSession,
    PerformanceSessionKind,
    Player,
    PlayerMonitoringProfile,
    PlayerPosition,
    RPEEntry,
    RPETrainingType,
    Staff,
    StaffRole,
    Team,
    PlayerTeamAssignment,
    WeightEntry,
    WellnessEntry,
)
from .permissions import ROLE_ADMIN, ROLE_READ_ONLY, ROLE_TRAINER


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
)
class DashboardPersistenceTests(TestCase):
    """Regression tests voor de belangrijkste MySQL-opslagflows."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="tester",
            password="test-pass",
            is_staff=True,
        )
        admin_group = Group.objects.create(name=ROLE_ADMIN)
        cls.user.groups.add(admin_group)
        cls.player = Player.objects.create(name="Test Speler")
        PlayerMonitoringProfile.objects.create(player=cls.player)
        cls.other_player = Player.objects.create(name="Andere Speler")

        AttendanceStatus.objects.create(code="overig", label="Overig", sort_order=1)
        AttendanceStatus.objects.create(code="fit", label="Fit", sort_order=2)
        RPETrainingType.objects.create(name="Training")

        PerformanceSessionKind.objects.create(code="test", label="Test")
        for code in (
            "sprint_10",
            "sprint_30",
            "cmj",
            "isrt",
            "submax",
            "curr_weight",
            "length",
            "sum_skinfolds",
        ):
            PerformanceMetricType.objects.create(
                code=code,
                label=code.replace("_", " ").title(),
                unit="",
                category="test",
            )

    def setUp(self):
        self.client.force_login(self.user)

    def test_login_required_for_dashboard(self):
        response = Client().get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])
        self.assertIn("next=/dashboard/", response["Location"])

    def test_dashboard_shows_home_agenda_and_risk_panel(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Verhoogd blessurerisico")
        self.assertContains(response, "Agenda")

    def test_academie_team_page_shows_team_environment(self):
        team = Team.objects.create(code="O17", name="O17")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team,
            start_date=date(2026, 1, 1),
        )

        response = self.client.get(reverse("academie_team", args=["O17"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GPS-data")
        self.assertContains(response, "Testdata")
        self.assertContains(response, "Wedstrijddata")
        self.assertContains(response, self.player.name)

    def test_wellness_post_creates_and_updates_one_entry_per_player_date(self):
        payload = {
            "player_id": self.player.id,
            "date": "2026-05-15",
            "sleep": "4",
            "mood": "3",
            "fitness": "5",
            "soreness": "2",
            "comment": "Goed hersteld",
        }

        response = self.client.post(reverse("wellness"), payload)

        self.assertEqual(response.status_code, 302)
        entry = WellnessEntry.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(entry.sleep, 4)
        self.assertEqual(entry.comment, "Goed hersteld")

        payload["sleep"] = "5"
        payload["comment"] = "Bijgewerkt"
        self.client.post(reverse("wellness"), payload)

        self.assertEqual(
            WellnessEntry.objects.filter(player=self.player, date=date(2026, 5, 15)).count(),
            1,
        )
        entry.refresh_from_db()
        self.assertEqual(entry.sleep, 5)
        self.assertEqual(entry.comment, "Bijgewerkt")

    def test_rpe_post_creates_and_updates_one_entry_per_player_date(self):
        training_type = RPETrainingType.objects.get(name="Training")
        payload = {
            "player_id": self.player.id,
            "date": "2026-05-15",
            "rpe": "7",
            "training_type": str(training_type.id),
        }

        response = self.client.post(reverse("rpe"), payload)

        self.assertEqual(response.status_code, 302)
        entry = RPEEntry.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(entry.rpe, 7)
        self.assertEqual(entry.training_type_ref, training_type)

        payload["rpe"] = "8"
        self.client.post(reverse("rpe"), payload)

        self.assertEqual(RPEEntry.objects.filter(player=self.player, date=date(2026, 5, 15)).count(), 1)
        entry.refresh_from_db()
        self.assertEqual(entry.rpe, 8)

    def test_testdata_post_persists_performance_session_metrics_and_updates(self):
        payload = {
            "player_id": self.player.id,
            "test_date": "2026-05-15",
            "sprint_10": "1.82",
            "sprint_30": "4.31",
            "cmj": "42.5",
            "isrt": "1780",
            "submax": "87.5",
            "curr_weight": "78.4",
            "length": "184.2",
            "sum_skinfolds": "48.1",
        }

        response = self.client.post(reverse("testdata"), payload)

        self.assertEqual(response.status_code, 302)
        session = PerformanceSession.objects.get(
            player=self.player,
            session_kind_ref__code="test",
            session_date=date(2026, 5, 15),
        )
        metrics = {metric.metric_type.code: metric.value for metric in session.metrics.all()}
        self.assertEqual(metrics["sprint_10"], 1.82)
        self.assertEqual(metrics["cmj"], 42.5)

        payload["sprint_10"] = "1.79"
        self.client.post(reverse("testdata"), payload)

        self.assertEqual(
            PerformanceSession.objects.filter(
                player=self.player,
                session_kind_ref__code="test",
                session_date=date(2026, 5, 15),
            ).count(),
            1,
        )
        metric = PerformanceMetric.objects.get(session=session, metric_type__code="sprint_10")
        self.assertEqual(metric.value, 1.79)

    def test_nutrition_intake_post_persists_and_updates_session_items(self):
        payload = {
            "player_id": self.player.id,
            "date": "2026-05-15",
            "goal": "Meer energie in ochtend",
            "next_meeting_goal": "Ontbijt evalueren",
            "breakfast": "Havermout",
            "snack1": "Banaan",
            "lunch": "Rijst met kip",
            "snack2": "Yoghurt",
            "dinner": "Pasta",
            "snack3": "Kwark",
            "supplements": "Vitamine D",
            "nutrition_focus": "Ontbijt consequent nemen",
        }

        response = self.client.post(reverse("nutrition"), payload)

        self.assertEqual(response.status_code, 302)
        session = NutritionIntakeSession.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(session.goal, "Meer energie in ochtend")
        self.assertEqual(session.items.count(), 7)
        self.assertEqual(
            NutritionIntakeItem.objects.get(session=session, meal_key="breakfast").value,
            "Havermout",
        )
        self.player.monitoring_profile.refresh_from_db()
        self.assertEqual(self.player.monitoring_profile.nutrition_focus, "Ontbijt consequent nemen")

        payload["goal"] = "Bijgewerkt doel"
        payload["breakfast"] = "Brood met ei"
        self.client.post(reverse("nutrition"), payload)

        self.assertEqual(
            NutritionIntakeSession.objects.filter(player=self.player, date=date(2026, 5, 15)).count(),
            1,
        )
        session.refresh_from_db()
        self.assertEqual(session.goal, "Bijgewerkt doel")
        self.assertEqual(session.items.count(), 7)
        self.assertEqual(
            NutritionIntakeItem.objects.get(session=session, meal_key="breakfast").value,
            "Brood met ei",
        )

    def test_weight_post_persists_weight_entry_and_monitoring_profile(self):
        payload = {
            "form_type": "weights",
            "weight_date": "2026-05-15",
            f"weight_{self.player.id}": "80.5",
            f"weight_{self.other_player.id}": "",
        }

        response = self.client.post(reverse("nutrition"), payload)

        self.assertEqual(response.status_code, 302)
        entry = WeightEntry.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(entry.weight, 80.5)

        payload[f"weight_{self.player.id}"] = "81.2"
        self.client.post(reverse("nutrition"), payload)

        self.assertEqual(WeightEntry.objects.filter(player=self.player, date=date(2026, 5, 15)).count(), 1)
        entry.refresh_from_db()
        self.assertEqual(entry.weight, 81.2)

    def test_attendance_page_creates_records_and_update_persists(self):
        response = self.client.get(reverse("aanwezigheden"), {"date": "2026-05-15"})

        self.assertEqual(response.status_code, 200)
        record = AttendanceRecord.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(record.status.code, "overig")
        self.assertFalse(record.completed)

        response = self.client.post(
            reverse("aanwezigheden_update", args=[record.id]),
            {"status": "fit", "completed": "on"},
        )

        self.assertEqual(response.status_code, 302)
        record.refresh_from_db()
        self.assertEqual(record.status.code, "fit")
        self.assertTrue(record.completed)

    def test_delete_weekday_requires_post_and_deletes_entry(self):
        day = DayProgramEntry.objects.create(
            date=date(2026, 5, 15),
            title="Training",
            activities="Veld",
        )

        get_response = self.client.get(reverse("delete_weekday", args=[day.id]))
        day.refresh_from_db()

        self.assertEqual(get_response.status_code, 302)
        self.assertTrue(DayProgramEntry.objects.filter(id=day.id).exists())

        post_response = self.client.post(reverse("delete_weekday", args=[day.id]))

        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(DayProgramEntry.objects.filter(id=day.id).exists())

    def test_add_weekday_persists_academy_agenda_fields(self):
        response = self.client.post(
            reverse("add_weekday"),
            {
                "date": "2026-05-21",
                "team": "O17",
                "category": "kracht",
                "context": "Opstart",
                "location": "Hengelo",
                "start_time": "09:00",
                "end_time": "11:00",
                "responsible": "Siebe",
                "physical_note": "Snel herstel",
                "activities": "Agenda-item",
                "notes": "Veld 1",
            },
        )

        self.assertEqual(response.status_code, 302)
        entry = DayProgramEntry.objects.get(date=date(2026, 5, 21), team="O17")
        self.assertEqual(entry.category, "kracht")
        self.assertEqual(entry.context, "Opstart")
        self.assertEqual(entry.location, "Hengelo")
        self.assertEqual(entry.start_time.strftime("%H:%M"), "09:00")
        self.assertEqual(entry.end_time.strftime("%H:%M"), "11:00")
        self.assertEqual(entry.responsible, "Siebe")
        self.assertEqual(entry.physical_note, "Snel herstel")

    def test_staf_page_admin_can_create_player(self):
        response = self.client.post(
            reverse("staf"),
            {
                "form_type": "add_player",
                "player_name": "Nieuwe Testspeler",
                "position_name": "Buitenspeler",
            },
        )

        self.assertEqual(response.status_code, 302)
        player = Player.objects.get(name="Nieuwe Testspeler")
        self.assertEqual(player.position_ref.name, "Buitenspeler")
        self.assertTrue(player.is_active)
        self.assertTrue(hasattr(player, "monitoring_profile"))

    def test_staf_page_admin_can_update_and_archive_player(self):
        position = PlayerPosition.objects.create(name="Middenvelder")
        player = Player.objects.create(name="Oude Speler", position_ref=position)

        response = self.client.post(
            reverse("staf"),
            {
                "form_type": "edit_player",
                "player_id": player.id,
                "player_name": "Nieuwe Speler",
                "position_name": "Buitenspeler",
            },
        )

        self.assertEqual(response.status_code, 302)
        player.refresh_from_db()
        self.assertEqual(player.name, "Nieuwe Speler")
        self.assertEqual(player.position_ref.name, "Buitenspeler")
        self.assertFalse(player.is_active)
        self.assertTrue(hasattr(player, "monitoring_profile"))

    def test_staf_page_admin_can_create_staff_user_with_dashboard_role(self):
        response = self.client.post(
            reverse("staf"),
            {
                "form_type": "add_staff",
                "name": "Medische Tester",
                "role_name": "Fysiotherapeut",
                "username": "medisch",
                "email": "medisch@example.test",
                "password": "temporary-pass-123",
                "dashboard_role": "Medisch",
            },
        )

        self.assertEqual(response.status_code, 302)
        staff = Staff.objects.select_related("role_ref", "user").get(name="Medische Tester")
        self.assertEqual(staff.role_ref.name, "Fysiotherapeut")
        self.assertEqual(staff.user.username, "medisch")
        self.assertTrue(staff.user.groups.filter(name="Medisch").exists())

    def test_staf_page_admin_can_update_staff_login_role_password_and_status(self):
        role = StaffRole.objects.create(name="Assistent")
        user = get_user_model().objects.create_user(
            username="coach",
            email="old@example.test",
            password="old-pass",
        )
        staff = Staff.objects.create(name="Oude Naam", role_ref=role, user=user)

        response = self.client.post(
            reverse("staf"),
            {
                "form_type": "edit_staff",
                "staff_id": staff.id,
                "name": "Nieuwe Naam",
                "role_name": "Trainer",
                "username": "coach",
                "email": "coach@example.test",
                "password": "new-pass-123",
                "dashboard_role": ROLE_TRAINER,
            },
        )

        self.assertEqual(response.status_code, 302)
        staff.refresh_from_db()
        user.refresh_from_db()
        self.assertEqual(staff.name, "Nieuwe Naam")
        self.assertEqual(staff.role_ref.name, "Trainer")
        self.assertEqual(user.email, "coach@example.test")
        self.assertTrue(user.check_password("new-pass-123"))
        self.assertFalse(user.is_active)
        self.assertTrue(user.groups.filter(name=ROLE_TRAINER).exists())

    def test_overig_structured_pages_persist_sections(self):
        pop_response = self.client.post(
            reverse("overig") + "?page=pop",
            {
                "situatie": "Sterke uitgangspositie",
                "doelen": "Eerste meters verbeteren",
                "reflectie": "Speler herkent focuspunt",
                "actieplan": "Wekelijks opvolgen",
            },
        )
        hp_response = self.client.post(
            reverse("overig") + "?page=hp",
            {"section": "focus", "text": "Speler A extra volgen"},
        )
        jeugd_response = self.client.post(
            reverse("overig") + "?page=jeugd",
            {"section": "leerlijn", "text": "Heldere ontwikkellijn"},
        )

        self.assertEqual(pop_response.status_code, 302)
        self.assertEqual(hp_response.status_code, 302)
        self.assertEqual(jeugd_response.status_code, 302)
        self.assertTrue(OverigNote.objects.filter(page_key="pop", section_key="actieplan").exists())
        self.assertTrue(OverigNote.objects.filter(page_key="hp", section_key="focus").exists())
        self.assertTrue(OverigNote.objects.filter(page_key="jeugd", section_key="leerlijn").exists())

    def test_fysiek_rapport_page_loads_without_uploaded_data(self):
        response = self.client.get(reverse("fysiek_rapport"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fysiek rapport")
        self.assertContains(response, "Weekoverzicht fysieke belasting")

    def test_mdo_tab_persists_player_note(self):
        response = self.client.post(
            reverse("individuele_programmas") + f"?player_id={self.player.id}&view=mdo",
            {
                "save_mdo_note": "1",
                "view": "mdo",
                "mdo_note": "Extra aandacht voor herstel na wedstrijd.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            OverigNote.objects.filter(
                note_type="note",
                page_key="mdo",
                section_key=f"player:{self.player.id}",
                text="Extra aandacht voor herstel na wedstrijd.",
            ).exists()
        )

        page = self.client.get(reverse("individuele_programmas") + f"?player_id={self.player.id}&view=mdo")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Multidisciplinair overleg")
        self.assertContains(page, "Weekstart fysieke status")

    def test_mdo_action_point_can_be_saved_and_completed(self):
        response = self.client.post(
            reverse("individuele_programmas") + f"?player_id={self.player.id}&view=mdo",
            {
                "save_mdo_action": "1",
                "view": "mdo",
                "mdo_action_title": "Herstelprotocol bespreken",
                "mdo_action_owner": "Performance",
                "mdo_action_deadline": "2026-05-22",
                "mdo_action_status": "red",
            },
        )

        self.assertEqual(response.status_code, 302)
        action = MDOActionPoint.objects.get(player=self.player, title="Herstelprotocol bespreken")
        self.assertEqual(action.owner, "Performance")
        self.assertEqual(action.status_color, "red")
        self.assertFalse(action.is_done)

        complete_response = self.client.post(
            reverse("individuele_programmas") + f"?player_id={self.player.id}&view=mdo",
            {
                "complete_mdo_action": "1",
                "view": "mdo",
                "action_id": action.id,
            },
        )

        self.assertEqual(complete_response.status_code, 302)
        action.refresh_from_db()
        self.assertTrue(action.is_done)

    def test_individual_page_shows_central_player_profile(self):
        response = self.client.get(reverse("individuele_programmas") + f"?player_id={self.player.id}")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Centraal spelerprofiel")
        self.assertContains(response, "GPS 7d")
        self.assertContains(response, "MDO")
        self.assertContains(response, reverse("testdata") + f"?player_id={self.player.id}")
        self.assertContains(response, "tab=profiel")

    def test_read_only_user_can_view_but_not_post(self):
        read_only = get_user_model().objects.create_user(username="readonly", password="test-pass")
        group = Group.objects.create(name=ROLE_READ_ONLY)
        read_only.groups.add(group)
        self.client.force_login(read_only)

        get_response = self.client.get(reverse("dashboard"))
        post_response = self.client.post(
            reverse("wellness"),
            {
                "player_id": self.player.id,
                "date": "2026-05-15",
                "sleep": "4",
            },
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 403)
