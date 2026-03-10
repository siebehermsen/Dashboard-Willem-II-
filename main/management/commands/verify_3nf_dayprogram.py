from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Controleert migratie van legacy DayProgram naar DayProgramEntry."

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
        legacy_count = self._count("main_dayprogram")
        new_count = self._count("main_dayprogramentry")

        self.stdout.write(self.style.SUCCESS("=== DayProgram 3NF Verificatie ==="))
        self.stdout.write(f"Legacy DayProgram records: {legacy_count}")
        self.stdout.write(f"Nieuwe DayProgramEntry records: {new_count}")
        self.stdout.write(self.style.SUCCESS("Table-based check afgerond."))
