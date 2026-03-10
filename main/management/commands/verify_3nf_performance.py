from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Controleert 3NF-v2/v3 backfill voor training, wedstrijd en testdata."

    def _table_exists(self, table_name: str) -> bool:
        return table_name in connection.introspection.table_names()

    def _count(self, table_name: str) -> int:
        if not self._table_exists(table_name):
            return 0
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row = cursor.fetchone()
        return int(row[0] if row else 0)

    def _count_session_kind(self, kind: str) -> int:
        if not self._table_exists("main_performancesession"):
            return 0
        if not self._table_exists("main_performancesessionkind"):
            return 0
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM main_performancesession s
                INNER JOIN main_performancesessionkind k
                    ON k.id = s.session_kind_ref_id
                WHERE k.code = %s
                """,
                [kind],
            )
            row = cursor.fetchone()
        return int(row[0] if row else 0)

    def handle(self, *args, **options):
        legacy_training = self._count("main_trainingdata")
        legacy_match = self._count("main_wedstrijddata")
        legacy_test = self._count("main_playertest")

        sessions_training = self._count_session_kind("training")
        sessions_match = self._count_session_kind("match")
        sessions_test = self._count_session_kind("test")
        metric_types = self._count("main_performancemetrictype")
        metrics = self._count("main_performancemetric")

        self.stdout.write(self.style.SUCCESS("=== Performance 3NF Verificatie ==="))
        self.stdout.write(f"Legacy TrainingData: {legacy_training}")
        self.stdout.write(f"Nieuwe PerformanceSession (training): {sessions_training}")
        self.stdout.write(f"Legacy WedstrijdData: {legacy_match}")
        self.stdout.write(f"Nieuwe PerformanceSession (match): {sessions_match}")
        self.stdout.write(f"Legacy PlayerTest: {legacy_test}")
        self.stdout.write(f"Nieuwe PerformanceSession (test): {sessions_test}")
        self.stdout.write(f"PerformanceMetricType records: {metric_types}")
        self.stdout.write(f"PerformanceMetric records: {metrics}")

        ok = True
        if sessions_training < legacy_training:
            ok = False
            self.stdout.write(self.style.WARNING("Training-sessions lager dan legacy."))
        if sessions_match < legacy_match:
            ok = False
            self.stdout.write(self.style.WARNING("Match-sessions lager dan legacy."))
        if sessions_test < legacy_test:
            ok = False
            self.stdout.write(self.style.WARNING("Test-sessions lager dan legacy."))
        if metrics == 0:
            ok = False
            self.stdout.write(self.style.WARNING("Geen metrics gevonden in nieuwe 3NF-laag."))

        if ok:
            self.stdout.write(self.style.SUCCESS("Performance backfill lijkt in orde."))
