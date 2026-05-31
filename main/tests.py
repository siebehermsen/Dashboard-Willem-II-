from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import (
    AttendanceRecord,
    AttendanceStatus,
    DayProgramEntry,
    InjuryCase,
    MDOActionPoint,
    NutritionIntakeItem,
    NutritionIntakeSession,
    OverigNote,
    Programma,
    ProgrammaOefening,
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
from .permissions import (
    ROLE_ADMIN,
    ROLE_FYSIO,
    ROLE_HEAD_PERFORMANCE,
    ROLE_PLAYER,
    ROLE_READ_ONLY,
    ROLE_STRENGTH_TRAINER,
    ROLE_TRAINER,
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
        admin_group = Group.objects.create(name=ROLE_ADMIN)
        cls.user.groups.add(admin_group)
        cls.player = Player.objects.create(name="Test Speler")
        PlayerMonitoringProfile.objects.create(player=cls.player)
        cls.other_player = Player.objects.create(name="Andere Speler")

        AttendanceStatus.objects.create(code="overig", label="Overig", sort_order=1)
        AttendanceStatus.objects.create(code="fit", label="Fit", sort_order=2)
        RPETrainingType.objects.create(name="Training")

        PerformanceSessionKind.objects.create(code="test", label="Test")
        PerformanceSessionKind.objects.create(code="training", label="Training")
        for code in (
            "sprint_10",
            "sprint_30",
            "cmj",
            "isrt",
            "submax",
            "curr_weight",
            "length",
            "sum_skinfolds",
            "total_distance",
            "hsd",
            "sprints",
            "load",
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
        self.assertContains(response, "Stafapp")
        self.assertContains(response, "Spelersapp")

    def test_staff_can_preview_player_app_mode(self):
        response = self.client.get(reverse("dashboard") + "?app_view=player")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preview voor")
        self.assertContains(response, "Spelersapp")
        self.assertContains(response, "Dagelijkse check en sessiebelasting invullen.")
        self.assertContains(response, "player_tab=data")
        self.assertContains(response, "player_tab=testdata")
        self.assertNotContains(response, "Slaap")
        self.assertContains(response, "app_view=staff")

    def test_player_app_dashboard_forms_save_wellness_and_rpe(self):
        wellness_response = self.client.post(
            reverse("dashboard") + "?app_view=player",
            {
                "form_type": "player_app_wellness",
                "player_id": self.player.id,
                "date": "2026-05-15",
                "sleep": "1",
                "mood": "2",
                "fitness": "3",
                "soreness": "2",
                "comment": "Direct vanuit spelersapp",
            },
        )

        rpe_response = self.client.post(
            reverse("dashboard") + "?app_view=player",
            {
                "form_type": "player_app_srpe",
                "player_id": self.player.id,
                "date": "2026-05-15",
                "srpe": "8",
            },
        )

        self.assertEqual(wellness_response.status_code, 302)
        self.assertEqual(rpe_response.status_code, 302)
        self.assertIn("app_view=player", wellness_response["Location"])
        self.assertIn("player_tab=wellness", wellness_response["Location"])
        self.assertIn("app_view=player", rpe_response["Location"])
        self.assertIn("player_tab=wellness", rpe_response["Location"])

        wellness = WellnessEntry.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(wellness.sleep, 1)
        self.assertEqual(wellness.mood, 2)
        self.assertEqual(wellness.fitness, 3)
        self.assertEqual(wellness.soreness, 2)
        self.assertEqual(wellness.comment, "Direct vanuit spelersapp")

        rpe = RPEEntry.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(rpe.rpe, 8)

    def test_player_app_dashboard_shows_own_trainingdata(self):
        player_user = get_user_model().objects.create_user(username="player-gps", password="test-pass")
        player_group = Group.objects.create(name=ROLE_PLAYER)
        player_user.groups.add(player_group)
        self.player.user = player_user
        self.player.save(update_fields=["user"])
        training_kind = PerformanceSessionKind.objects.get(code="training")
        session = PerformanceSession.objects.create(
            player=self.player,
            session_kind_ref=training_kind,
            session_date=date(2026, 5, 15),
            week=20,
            source_legacy_table="test",
            source_legacy_id=1,
        )
        for code, value in {
            "total_distance": 5306,
            "hsd": 251,
            "sprints": 17,
            "load": 400,
        }.items():
            PerformanceMetric.objects.create(
                session=session,
                metric_type=PerformanceMetricType.objects.get(code=code),
                value=value,
            )

        self.client.force_login(player_user)
        response = self.client.get(reverse("dashboard") + "?app_view=player&player_tab=data")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mijn trainingsdata")
        self.assertContains(response, "5,3 km")
        self.assertContains(response, "251,0 m")
        self.assertContains(response, "17")
        self.assertNotContains(response, "dashboardPlayerSelect")

    def test_player_app_dashboard_shows_own_testdata(self):
        player_user = get_user_model().objects.create_user(username="player-testdata", password="test-pass")
        player_group, _ = Group.objects.get_or_create(name=ROLE_PLAYER)
        player_user.groups.add(player_group)
        self.player.user = player_user
        self.player.save(update_fields=["user"])
        test_kind = PerformanceSessionKind.objects.get(code="test")
        session = PerformanceSession.objects.create(
            player=self.player,
            session_kind_ref=test_kind,
            session_date=date(2026, 5, 16),
            week=20,
            source_legacy_table="test",
            source_legacy_id=2,
        )
        for code, value in {
            "sprint_10": 1.72,
            "sprint_30": 4.35,
            "cmj": 41.2,
            "isrt": 122,
            "curr_weight": 76.4,
            "length": 183,
        }.items():
            PerformanceMetric.objects.create(
                session=session,
                metric_type=PerformanceMetricType.objects.get(code=code),
                value=value,
            )

        self.client.force_login(player_user)
        response = self.client.get(reverse("dashboard") + "?app_view=player&player_tab=testdata")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Terug")
        self.assertContains(response, "Mijn testdata")
        self.assertContains(response, "dashboardPlayerTestChart")
        self.assertContains(response, "30 meter")
        self.assertContains(response, "CMJ")
        self.assertContains(response, "ISRT")
        self.assertContains(response, "1,72 s")
        self.assertNotContains(response, "dashboard-player-test-row")
        self.assertNotContains(response, "dashboardPlayerSelect")

    def test_player_app_dashboard_shows_own_potential_environment(self):
        player_user = get_user_model().objects.create_user(username="player-potential", password="test-pass")
        player_group, _ = Group.objects.get_or_create(name=ROLE_PLAYER)
        player_user.groups.add(player_group)
        self.player.user = player_user
        self.player.save(update_fields=["user"])
        OverigNote.objects.create(
            note_type="potential",
            page_key="potentials",
            section_key=f"player:{self.player.id}",
            text="High Potential",
        )
        Programma.objects.create(
            player=self.player,
            doel="Eigen versnelling verbeteren",
            plan_komende_periode="Twee blokken per week",
            ontwikkelaanpak="Sprintprogressie met video",
        )
        OverigNote.objects.create(
            note_type="note",
            page_key="potentials",
            section_key=f"player:{self.player.id}",
            text="Eigen aandachtspunt in de eerste meters.",
        )
        OverigNote.objects.create(
            note_type="potential",
            page_key="potentials",
            section_key=f"player:{self.other_player.id}",
            text="High Potential",
        )
        Programma.objects.create(
            player=self.other_player,
            doel="Verborgen programma andere speler",
        )

        self.client.force_login(player_user)
        home_response = self.client.get(reverse("dashboard") + "?app_view=player")
        detail_response = self.client.get(reverse("dashboard") + "?app_view=player&player_tab=potential")

        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, "player_tab=potential")
        self.assertContains(home_response, "Potential")
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Mijn Potential omgeving")
        self.assertContains(detail_response, "Eigen versnelling verbeteren")
        self.assertContains(detail_response, "Eigen aandachtspunt in de eerste meters.")
        self.assertNotContains(detail_response, "Verborgen programma andere speler")
        self.assertNotContains(detail_response, "dashboardPlayerSelect")

    def test_player_user_testdata_page_only_shows_own_profile(self):
        player_user = get_user_model().objects.create_user(username="player-testdata-page", password="test-pass")
        player_group, _ = Group.objects.get_or_create(name=ROLE_PLAYER)
        player_user.groups.add(player_group)
        self.player.user = player_user
        self.player.save(update_fields=["user"])

        test_kind = PerformanceSessionKind.objects.get(code="test")
        own_session = PerformanceSession.objects.create(
            player=self.player,
            session_kind_ref=test_kind,
            session_date=date(2026, 5, 16),
            source_legacy_table="test",
            source_legacy_id=20,
        )
        other_session = PerformanceSession.objects.create(
            player=self.other_player,
            session_kind_ref=test_kind,
            session_date=date(2026, 5, 16),
            source_legacy_table="test",
            source_legacy_id=21,
        )
        metric_type = PerformanceMetricType.objects.get(code="sprint_10")
        PerformanceMetric.objects.create(session=own_session, metric_type=metric_type, value=1.72)
        PerformanceMetric.objects.create(session=other_session, metric_type=metric_type, value=1.88)

        self.client.force_login(player_user)
        response = self.client.get(reverse("testdata"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)
        self.assertNotContains(response, "Kies team")
        self.assertNotContains(response, "Testdata invoeren")
        self.assertNotContains(response, "Teamoverzicht testdata")
        self.assertNotContains(response, "-- Kies een speler --")

    def test_dashboard_agenda_can_show_requested_week(self):
        DayProgramEntry.objects.create(
            date=date(2026, 6, 3),
            team="O17",
            category="training",
            context="Opstart",
            activities="Agenda-item",
        )

        response = self.client.get(reverse("dashboard") + "?week=2026-06-01")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "01-06-2026 t/m 07-06-2026")
        self.assertContains(response, "Opstart")
        self.assertContains(response, "?week=2026-05-25")
        self.assertContains(response, "?week=2026-06-08")

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

        player_response = self.client.get(reverse("academie_player", args=["O17", self.player.id]))
        self.assertEqual(player_response.status_code, 200)
        self.assertContains(player_response, "Laatste 7 dagen")
        self.assertContains(player_response, "academyPlayerGpsChart")

    def test_academie_old_players_environment_shows_archived_players(self):
        old_player = Player.objects.create(name="Oude Testspeler", is_active=False)

        response = self.client.get(reverse("academie_team", args=["OUD"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oud spelers")
        self.assertContains(response, old_player.name)
        self.assertNotContains(response, "O16")

        player_response = self.client.get(reverse("academie_player", args=["OUD", old_player.id]))
        self.assertEqual(player_response.status_code, 200)
        self.assertContains(player_response, "Oud spelers")
        self.assertContains(player_response, old_player.name)

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

    def test_wellness_filters_players_by_team_layout(self):
        team_o17 = Team.objects.create(code="O17", name="O17")
        team_o19 = Team.objects.create(code="O19", name="O19")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team_o17,
            start_date=date(2026, 1, 1),
        )
        PlayerTeamAssignment.objects.create(
            player=self.other_player,
            team=team_o19,
            start_date=date(2026, 1, 1),
        )

        response = self.client.get(reverse("wellness"), {"date": "2026-05-15", "team": "O17"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teams")
        self.assertContains(response, "Wellness")
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)

    def test_player_app_user_only_sees_and_saves_own_wellness(self):
        player_user = get_user_model().objects.create_user(username="player-login", password="test-pass")
        player_group = Group.objects.create(name=ROLE_PLAYER)
        player_user.groups.add(player_group)
        self.player.user = player_user
        self.player.save(update_fields=["user"])
        self.client.force_login(player_user)

        response = self.client.get(reverse("wellness"), {"date": "2026-05-15"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)

        own_response = self.client.post(
            reverse("wellness"),
            {
                "player_id": self.player.id,
                "date": "2026-05-15",
                "sleep": "2",
                "mood": "2",
                "fitness": "2",
                "soreness": "1",
                "srpe": "6",
                "comment": "Eigen invoer",
            },
        )
        other_response = self.client.post(
            reverse("wellness"),
            {
                "player_id": self.other_player.id,
                "date": "2026-05-15",
                "sleep": "2",
                "mood": "2",
                "fitness": "2",
                "soreness": "1",
                "comment": "Niet toegestaan",
            },
        )

        self.assertEqual(own_response.status_code, 302)
        self.assertEqual(other_response.status_code, 403)
        self.assertTrue(
            WellnessEntry.objects.filter(
                player=self.player,
                date=date(2026, 5, 15),
                comment="Eigen invoer",
            ).exists()
        )
        self.assertFalse(WellnessEntry.objects.filter(player=self.other_player).exists())

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

    def test_testdata_filters_player_select_by_academy_team(self):
        team_o17 = Team.objects.create(code="O17", name="O17")
        team_o19 = Team.objects.create(code="O19", name="O19")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team_o17,
            start_date=date(2026, 1, 1),
        )
        PlayerTeamAssignment.objects.create(
            player=self.other_player,
            team=team_o19,
            start_date=date(2026, 1, 1),
        )

        response = self.client.get(reverse("testdata") + "?team=O17&tab=invoer")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kies team")
        self.assertContains(response, "O17")
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)
        self.assertNotContains(response, "Oud spelers")

    def test_revalidatie_filters_player_select_by_academy_team(self):
        team_o17 = Team.objects.create(code="O17", name="O17")
        team_o19 = Team.objects.create(code="O19", name="O19")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team_o17,
            start_date=date(2026, 1, 1),
        )
        PlayerTeamAssignment.objects.create(
            player=self.other_player,
            team=team_o19,
            start_date=date(2026, 1, 1),
        )

        response = self.client.get(reverse("revalidatie") + "?team=O17")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kies team")
        self.assertContains(response, "O17")
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)
        self.assertNotContains(response, "Oud spelers")

    def test_academie_team_shows_current_revalidations_for_selected_team(self):
        team_o17 = Team.objects.create(code="O17", name="O17")
        team_o19 = Team.objects.create(code="O19", name="O19")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team_o17,
            start_date=date(2026, 1, 1),
        )
        PlayerTeamAssignment.objects.create(
            player=self.other_player,
            team=team_o19,
            start_date=date(2026, 1, 1),
        )
        InjuryCase.objects.create(
            player=self.player,
            started_on=date(2026, 5, 1),
            expected_return_on=date(2026, 5, 30),
        )
        InjuryCase.objects.create(
            player=self.other_player,
            started_on=date(2026, 5, 1),
            expected_return_on=date(2026, 5, 30),
        )

        response = self.client.get(reverse("academie_team", args=["O17"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Huidige revalidaties")
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)

    def test_individuele_programmas_filters_players_by_academy_team(self):
        team_o17 = Team.objects.create(code="O17", name="O17")
        team_o19 = Team.objects.create(code="O19", name="O19")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team_o17,
            start_date=date(2026, 1, 1),
        )
        PlayerTeamAssignment.objects.create(
            player=self.other_player,
            team=team_o19,
            start_date=date(2026, 1, 1),
        )

        response = self.client.get(reverse("individuele_programmas") + "?team=O17")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spelers O17")
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)

    def test_gps_training_upload_rejects_duplicate_player_date_rows(self):
        team = Team.objects.create(code="O17", name="O17")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team,
            start_date=date(2026, 1, 1),
        )
        csv_content = (
            "Player Last Name,Session Date,Total Distance,HIR (M>20 KM/U),Sprints\n"
            "Speler,15/05/2026,5306,251,17\n"
        ).encode("utf-8")

        first_response = self.client.post(
            reverse("upload_file"),
            {
                "upload_team": "O17",
                "upload_event": "opstart_training",
                "file": SimpleUploadedFile("training.csv", csv_content, content_type="text/csv"),
            },
        )
        second_response = self.client.post(
            reverse("upload_file"),
            {
                "upload_team": "O17",
                "upload_event": "opstart_training",
                "file": SimpleUploadedFile("training.csv", csv_content, content_type="text/csv"),
            },
        )

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 302)
        self.assertEqual(
            PerformanceSession.objects.filter(
                player=self.player,
                session_kind_ref__code="training",
                session_date=date(2026, 5, 15),
            ).count(),
            1,
        )
        message_text = " ".join(str(message) for message in get_messages(second_response.wsgi_request))
        self.assertIn("dubbele O17 opstart trainingregel", message_text)

    def test_training_upload_prefills_event_from_agenda(self):
        team = Team.objects.create(code="O17", name="O17")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team,
            start_date=date(2026, 1, 1),
        )
        DayProgramEntry.objects.create(
            date=timezone.localdate(),
            title="Training O17",
            team="O17",
            category="training",
        )

        response = self.client.get(reverse("training"), {"team": "O17"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Agenda-suggesties")
        self.assertContains(response, "O17 · Opstart training")
        self.assertContains(response, "Agenda-items voor O17")
        self.assertContains(response, "Training")
        self.assertContains(response, 'value="opstart_training" selected')

    def test_match_upload_prefills_event_from_agenda(self):
        team = Team.objects.create(code="O19", name="O19")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team,
            start_date=date(2026, 1, 1),
        )
        DayProgramEntry.objects.create(
            date=timezone.localdate(),
            title="Competitiewedstrijd O19",
            team="O19",
            category="wedstrijd",
        )

        response = self.client.get(reverse("wedstrijddata"), {"team": "O19"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "O19 · Competitiewedstrijd")
        self.assertContains(response, 'value="competitiewedstrijd" selected')

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
        team = Team.objects.create(code="O17", name="O17")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team,
            start_date=date(2026, 1, 1),
        )

        response = self.client.get(reverse("aanwezigheden"), {"date": "2026-05-15", "team": "O17"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teams")
        self.assertContains(response, "O17")
        self.assertContains(response, self.player.name)
        record = AttendanceRecord.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(record.status.code, "overig")
        self.assertFalse(record.completed)

        response = self.client.post(
            reverse("aanwezigheden_update", args=[record.id]),
            {"status": "fit", "completed": "on", "team": "O17"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("team=O17", response["Location"])
        record.refresh_from_db()
        self.assertEqual(record.status.code, "fit")
        self.assertTrue(record.completed)

    def test_attendance_page_filters_players_by_team(self):
        team_o17 = Team.objects.create(code="O17", name="O17")
        team_o19 = Team.objects.create(code="O19", name="O19")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team_o17,
            start_date=date(2026, 1, 1),
        )
        PlayerTeamAssignment.objects.create(
            player=self.other_player,
            team=team_o19,
            start_date=date(2026, 1, 1),
        )

        response = self.client.get(reverse("aanwezigheden"), {"date": "2026-05-15", "team": "O17"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.player.name)
        self.assertNotContains(response, self.other_player.name)

    def test_attendance_page_uses_agenda_training_as_default_status(self):
        team = Team.objects.create(code="O17", name="O17")
        PlayerTeamAssignment.objects.create(
            player=self.player,
            team=team,
            start_date=date(2026, 1, 1),
        )
        DayProgramEntry.objects.create(
            date=date(2026, 5, 15),
            title="O17 training",
            team="O17",
            category="training",
        )

        response = self.client.get(reverse("aanwezigheden"), {"date": "2026-05-15", "team": "O17"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Training O17")
        record = AttendanceRecord.objects.get(player=self.player, date=date(2026, 5, 15))
        self.assertEqual(record.status.code, "training_o17")

    def test_full_staff_roles_can_open_performance_pages_but_not_staf(self):
        for role in (ROLE_HEAD_PERFORMANCE, ROLE_FYSIO, ROLE_STRENGTH_TRAINER):
            with self.subTest(role=role):
                user = get_user_model().objects.create_user(
                    username=f"role-{role.lower().replace(' ', '-')}",
                    password="test-pass",
                )
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)
                self.client.force_login(user)

                self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)
                self.assertEqual(self.client.get(reverse("training")).status_code, 200)
                self.assertEqual(self.client.get(reverse("testdata")).status_code, 200)
                self.assertEqual(self.client.get(reverse("wellness")).status_code, 200)
                self.assertEqual(self.client.get(reverse("aanwezigheden"), {"date": "2026-05-15"}).status_code, 200)
                self.assertEqual(self.client.get(reverse("revalidatie")).status_code, 200)
                self.assertEqual(self.client.get(reverse("nutrition")).status_code, 200)
                self.assertEqual(self.client.get(reverse("potentials")).status_code, 200)
                self.assertEqual(self.client.get(reverse("staf")).status_code, 403)

    def test_teamtrainer_has_limited_academy_permissions(self):
        trainer_user = get_user_model().objects.create_user(
            username="teamtrainer",
            password="test-pass",
        )
        trainer_group, _ = Group.objects.get_or_create(name=ROLE_TRAINER)
        trainer_user.groups.add(trainer_group)
        self.client.force_login(trainer_user)

        self.assertEqual(self.client.get(reverse("testdata")).status_code, 200)
        self.assertEqual(self.client.get(reverse("training")).status_code, 200)
        self.assertEqual(self.client.get(reverse("wellness")).status_code, 200)
        self.assertEqual(self.client.get(reverse("individuele_programmas")).status_code, 200)
        self.assertEqual(self.client.get(reverse("potentials")).status_code, 200)
        self.assertEqual(self.client.get(reverse("aanwezigheden")).status_code, 403)
        self.assertEqual(self.client.get(reverse("nutrition")).status_code, 403)
        self.assertEqual(self.client.get(reverse("revalidatie")).status_code, 403)
        self.assertEqual(self.client.get(reverse("beweeganalyse")).status_code, 403)
        self.assertEqual(self.client.get(reverse("staf")).status_code, 403)

    def test_fysio_can_open_rehab_but_not_staf(self):
        fysio_user = get_user_model().objects.create_user(
            username="fysio",
            password="test-pass",
        )
        fysio_group, _ = Group.objects.get_or_create(name=ROLE_FYSIO)
        fysio_user.groups.add(fysio_group)
        self.client.force_login(fysio_user)

        self.assertEqual(self.client.get(reverse("revalidatie")).status_code, 200)
        self.assertEqual(self.client.get(reverse("staf")).status_code, 403)

    def test_player_role_is_limited_to_own_app_and_own_data(self):
        player_user = get_user_model().objects.create_user(
            username="player-locked",
            password="test-pass",
        )
        player_group, _ = Group.objects.get_or_create(name=ROLE_PLAYER)
        player_user.groups.add(player_group)
        self.player.user = player_user
        self.player.save(update_fields=["user"])
        WellnessEntry.objects.create(
            player=self.player,
            date=date(2026, 5, 15),
            sleep=3,
            mood=3,
            fitness=3,
            soreness=2,
        )
        WellnessEntry.objects.create(
            player=self.other_player,
            date=date(2026, 5, 15),
            sleep=1,
            mood=1,
            fitness=1,
            soreness=3,
            comment="Mag niet zichtbaar zijn",
        )
        self.client.force_login(player_user)

        dashboard_response = self.client.get(reverse("dashboard") + "?app_view=staff")
        wellness_response = self.client.get(reverse("wellness"), {"date": "2026-05-15"})
        testdata_response = self.client.get(reverse("testdata") + f"?player_id={self.player.id}")

        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, "Spelersapp")
        self.assertNotContains(dashboard_response, "Stafapp")
        self.assertNotContains(dashboard_response, 'href="/academie/')
        self.assertEqual(wellness_response.status_code, 200)
        self.assertContains(wellness_response, self.player.name)
        self.assertNotContains(wellness_response, self.other_player.name)
        self.assertNotContains(wellness_response, "Teams")
        self.assertEqual(testdata_response.status_code, 200)
        self.assertNotContains(testdata_response, "Kies team")
        self.assertNotContains(testdata_response, "Teamoverzicht testdata")
        self.assertEqual(self.client.get(reverse("staf")).status_code, 403)
        self.assertEqual(self.client.get(reverse("training")).status_code, 403)
        self.assertEqual(self.client.get(reverse("academie_team", args=["O21"])).status_code, 403)
        self.assertEqual(self.client.get(reverse("aanwezigheden")).status_code, 403)
        self.assertEqual(self.client.get(reverse("revalidatie")).status_code, 403)

    def test_player_data_endpoints_are_limited_to_own_player(self):
        player_user = get_user_model().objects.create_user(
            username="own-player",
            password="test-pass",
        )
        player_group, _ = Group.objects.get_or_create(name=ROLE_PLAYER)
        player_user.groups.add(player_group)
        self.player.user = player_user
        self.player.save(update_fields=["user"])
        self.client.force_login(player_user)

        own_response = self.client.get(reverse("player_data", args=[self.player.id]))
        other_response = self.client.get(reverse("player_data", args=[self.other_player.id]))

        self.assertEqual(own_response.status_code, 200)
        self.assertEqual(other_response.status_code, 403)

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

    def test_edit_weekday_updates_academy_agenda_fields(self):
        entry = DayProgramEntry.objects.create(
            date=date(2026, 5, 21),
            team="O17",
            category="training",
            activities="Agenda-item",
        )

        response = self.client.post(
            reverse("edit_weekday", args=[entry.id]),
            {
                "date": "2026-05-22",
                "team": "O19",
                "category": "data",
                "context": "GPS upload",
                "location": "Kantoor",
                "start_time": "11:15",
                "end_time": "11:45",
                "responsible": "Performance",
                "physical_note": "Data klaarzetten",
                "activities": "Agenda-item",
                "notes": "Na training",
            },
        )

        self.assertEqual(response.status_code, 302)
        entry.refresh_from_db()
        self.assertEqual(entry.date, date(2026, 5, 22))
        self.assertEqual(entry.team, "O19")
        self.assertEqual(entry.category, "data")
        self.assertEqual(entry.context, "GPS upload")
        self.assertEqual(entry.location, "Kantoor")
        self.assertEqual(entry.start_time.strftime("%H:%M"), "11:15")
        self.assertEqual(entry.end_time.strftime("%H:%M"), "11:45")
        self.assertEqual(entry.responsible, "Performance")
        self.assertEqual(entry.physical_note, "Data klaarzetten")
        self.assertEqual(entry.notes, "Na training")

    def test_staf_page_admin_can_create_player(self):
        response = self.client.post(
            reverse("staf"),
            {
                "form_type": "add_player",
                "player_name": "Nieuwe Testspeler",
                "position_name": "Buitenspeler",
                "team_code": "O17",
            },
        )

        self.assertEqual(response.status_code, 302)
        player = Player.objects.get(name="Nieuwe Testspeler")
        self.assertEqual(player.position_ref.name, "Buitenspeler")
        self.assertTrue(player.is_active)
        self.assertTrue(hasattr(player, "monitoring_profile"))
        assignment = PlayerTeamAssignment.objects.select_related("team").get(player=player)
        self.assertEqual(assignment.team.code, "O17")

    def test_staf_page_admin_can_update_player_to_old_players(self):
        position = PlayerPosition.objects.create(name="Middenvelder")
        player = Player.objects.create(name="Oude Speler", position_ref=position)

        response = self.client.post(
            reverse("staf"),
            {
                "form_type": "edit_player",
                "player_id": player.id,
                "player_name": "Nieuwe Speler",
                "position_name": "Buitenspeler",
                "team_code": "OUD",
                "is_active": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        player.refresh_from_db()
        self.assertEqual(player.name, "Nieuwe Speler")
        self.assertEqual(player.position_ref.name, "Buitenspeler")
        self.assertFalse(player.is_active)
        self.assertTrue(hasattr(player, "monitoring_profile"))
        assignment = PlayerTeamAssignment.objects.select_related("team").get(player=player)
        self.assertEqual(assignment.team.code, "OUD")

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
                "dashboard_role": ROLE_FYSIO,
            },
        )

        self.assertEqual(response.status_code, 302)
        staff = Staff.objects.select_related("role_ref", "user").get(name="Medische Tester")
        self.assertEqual(staff.role_ref.name, "Fysiotherapeut")
        self.assertEqual(staff.user.username, "medisch")
        self.assertTrue(staff.user.groups.filter(name=ROLE_FYSIO).exists())

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
        fotos_response = self.client.get(reverse("overig") + "?page=fotos")
        hit_response = self.client.get(reverse("overig_hit"))

        self.assertEqual(pop_response.status_code, 302)
        self.assertEqual(hp_response.status_code, 302)
        self.assertEqual(fotos_response.status_code, 200)
        self.assertEqual(hit_response.status_code, 200)
        self.assertTrue(OverigNote.objects.filter(page_key="pop", section_key="actieplan").exists())
        self.assertTrue(OverigNote.objects.filter(page_key="hp", section_key="focus").exists())
        self.assertContains(fotos_response, "Foto's uploaden")
        self.assertContains(hit_response, "HIT Calculator")

    def test_fysiek_rapport_page_loads_without_uploaded_data(self):
        response = self.client.get(reverse("fysiek_rapport"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fysiek rapport")
        self.assertContains(response, "O21 fysiek rapport")
        self.assertContains(response, "Kies team")
        self.assertContains(response, "O12")
        self.assertNotContains(response, "Oud spelers")
        self.assertNotContains(response, "O16")
        self.assertNotContains(response, "Speler fysiek rapport")

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

    def test_potentials_page_can_add_player_program_and_attention(self):
        add_response = self.client.post(
            reverse("potentials"),
            {
                "action": "add_existing",
                "player_id": self.player.id,
            },
        )

        self.assertEqual(add_response.status_code, 302)
        self.assertTrue(
            OverigNote.objects.filter(
                note_type="potential",
                page_key="potentials",
                section_key=f"player:{self.player.id}",
            ).exists()
        )

        program_response = self.client.post(
            reverse("potentials"),
            {
                "action": "save_program",
                "selected_player_id": self.player.id,
                "doel": "Eerste meters dominanter maken",
                "sterke_punten": "Explosief",
                "verbeterpunten": "Open lichaamshouding",
                "plan_komende_periode": "Twee veldblokken per week",
                "fysiek_ontwikkelpunt": "Acceleratie",
                "ontwikkelaanpak": "Sprintprogressie met video",
            },
        )
        attention_response = self.client.post(
            reverse("potentials"),
            {
                "action": "add_attention",
                "selected_player_id": self.player.id,
                "attention_text": "Meer scannen voor de eerste aanname.",
                "attention_date": "2026-05-27",
                "attention_owner": "Trainer",
                "attention_status": "mee_bezig",
            },
        )
        exercise_response = self.client.post(
            reverse("potentials"),
            {
                "action": "add_exercise",
                "selected_player_id": self.player.id,
                "exercise_name": "Resisted sprint 10m",
                "exercise_duration": "12",
                "exercise_rpe": "7",
                "exercise_frequency": "2x per week",
                "exercise_notes": "Volledige rust tussen herhalingen.",
            },
        )
        strength_response = self.client.post(
            reverse("potentials"),
            {
                "action": "save_strength_program",
                "selected_player_id": self.player.id,
                "strength_thema": "Explosieve kracht",
                "strength_frequentie": "2x per week",
                "strength_doelstelling": "Meer kracht in de eerste meters.",
                "strength_evaluatie": "Evalueren na vier weken met sprinttest.",
            },
        )

        self.assertEqual(program_response.status_code, 302)
        self.assertEqual(attention_response.status_code, 302)
        self.assertEqual(exercise_response.status_code, 302)
        self.assertEqual(strength_response.status_code, 302)
        self.assertTrue(Programma.objects.filter(player=self.player, doel="Eerste meters dominanter maken").exists())
        self.assertTrue(
            OverigNote.objects.filter(
                note_type="note",
                page_key="potentials",
                section_key=f"player:{self.player.id}",
                text__contains="Meer scannen voor de eerste aanname.",
            ).exists()
        )
        self.assertTrue(
            OverigNote.objects.filter(
                note_type="note",
                page_key="potentials",
                section_key=f"player:{self.player.id}",
                text__contains="mee_bezig",
            ).exists()
        )
        self.assertTrue(ProgrammaOefening.objects.filter(programma__player=self.player, naam_ref__name="Resisted sprint 10m").exists())
        self.assertTrue(
            OverigNote.objects.filter(
                note_type="section",
                page_key="potentials",
                section_key=f"strength:{self.player.id}",
                text__contains="Explosieve kracht",
            ).exists()
        )
        ajax_response = self.client.post(
            reverse("potentials"),
            {
                "action": "save_strength_program",
                "selected_player_id": self.player.id,
                "strength_thema": "Maximale kracht",
                "strength_frequentie": "1x per week",
                "strength_doelstelling": "Robuuster worden in duels.",
                "strength_evaluatie": "Elke maand evalueren.",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(ajax_response.status_code, 200)
        self.assertEqual(ajax_response.json()["message"], "Succesvol opgeslagen. Krachtprogramma bijgewerkt.")

        page = self.client.get(reverse("potentials") + f"?player_id={self.player.id}")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Potentials")
        self.assertContains(page, "Overzicht")
        self.assertContains(page, "Testdata")
        self.assertContains(page, "GPS-data")
        self.assertContains(page, "Aanwezigheid")
        self.assertContains(page, "Lengte en gewicht")
        self.assertContains(page, "Beweeganalyse")
        self.assertContains(page, "Krachtprogramma")
        self.assertContains(page, "Open volledig fysiek profiel")
        self.assertContains(page, "Eerste meters dominanter maken")
        self.assertContains(page, "Meer scannen voor de eerste aanname.")
        self.assertContains(page, "Mee bezig")
        self.assertContains(page, "Trainer")
        self.assertContains(page, "Maximale kracht")

        home = self.client.get(reverse("potentials"))
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "Klik op een speler om zijn individuele Potentials-omgeving te openen.")
        self.assertNotContains(home, "Individueel programma")

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
