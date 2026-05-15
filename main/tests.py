from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import (
    AttendanceRecord,
    AttendanceStatus,
    DayProgramEntry,
    NutritionIntakeItem,
    NutritionIntakeSession,
    PerformanceMetric,
    PerformanceMetricType,
    PerformanceSession,
    PerformanceSessionKind,
    Player,
    PlayerMonitoringProfile,
    RPEEntry,
    RPETrainingType,
    WeightEntry,
    WellnessEntry,
)


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
