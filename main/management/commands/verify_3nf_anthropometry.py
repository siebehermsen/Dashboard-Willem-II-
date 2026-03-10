from django.core.management.base import BaseCommand
from django.db import connection

from main.models import AnthropometryMeasurement, AnthropometrySession


class Command(BaseCommand):
    help = "Controleert backfill/sync voor antropometrie 3NF-v2."

    def _table_exists(self, table_name: str) -> bool:
        return table_name in connection.introspection.table_names()

    def _legacy_count(self) -> int:
        if not self._table_exists("main_antropometry"):
            return 0
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM main_antropometry")
            row = cursor.fetchone()
        return int(row[0] if row else 0)

    def handle(self, *args, **options):
        legacy_count = self._legacy_count()
        session_count = AnthropometrySession.objects.count()
        measurement_count = AnthropometryMeasurement.objects.count()

        self.stdout.write(self.style.SUCCESS("=== Anthropometry 3NF Verificatie ==="))
        self.stdout.write(f"Legacy Antropometry records: {legacy_count}")
        self.stdout.write(f"Nieuwe AnthropometrySession records: {session_count}")
        self.stdout.write(f"Nieuwe AnthropometryMeasurement records: {measurement_count}")

        if session_count < legacy_count:
            self.stdout.write(self.style.WARNING("Let op: minder sessions dan legacy records. Check datums/spelerkoppeling."))
        else:
            self.stdout.write(self.style.SUCCESS("Session-aantallen lijken consistent of completer dan legacy."))
