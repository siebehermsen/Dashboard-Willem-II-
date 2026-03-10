from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Controleert backfill/sync voor Overig 3NF-v2."

    def _table_exists(self, table_name: str) -> bool:
        return table_name in connection.introspection.table_names()

    def _count(self, table_name: str) -> int:
        if not self._table_exists(table_name):
            return 0
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row = cursor.fetchone()
        return int(row[0] if row else 0)

    def handle(self, *args, **options):
        legacy_count = self._count("main_overig")
        new_count = self._count("main_overignote")

        self.stdout.write(self.style.SUCCESS("=== Overig 3NF Verificatie ==="))
        self.stdout.write(f"Legacy Overig records: {legacy_count}")
        self.stdout.write(f"Nieuwe OverigNote records: {new_count}")

        if legacy_count > 0 and new_count == 0:
            self.stdout.write(self.style.WARNING("Let op: backfill lijkt niet uitgevoerd."))
        else:
            self.stdout.write(self.style.SUCCESS("Overig backfill lijkt in orde."))
