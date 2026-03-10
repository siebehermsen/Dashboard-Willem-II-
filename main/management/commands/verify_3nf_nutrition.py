from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Controleert nutrition 3NF-v2 backfill en aantallen."

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
        legacy = self._count("main_playerintake")
        sessions = self._count("main_nutritionintakesession")
        items = self._count("main_nutritionintakeitem")

        self.stdout.write(self.style.SUCCESS("=== Nutrition 3NF Verificatie ==="))
        self.stdout.write(f"Legacy PlayerIntake records: {legacy}")
        self.stdout.write(f"Nieuwe NutritionIntakeSession records: {sessions}")
        self.stdout.write(f"Nieuwe NutritionIntakeItem records: {items}")
        if sessions < legacy:
            self.stdout.write(self.style.WARNING("Sessions lager dan legacy. Controleer backfill/migratie."))
        else:
            self.stdout.write(self.style.SUCCESS("Session-aantallen zijn consistent of hoger dan legacy."))
