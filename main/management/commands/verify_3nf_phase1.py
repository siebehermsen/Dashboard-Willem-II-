from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Controleert fase-1 3NF migratie voor InjuryCase en HitWeekPlan."

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
        old_injury_count = self._count("main_injury")
        new_injury_count = self._count("main_injurycase")
        old_hit_count = self._count("main_hitweekplanning")
        new_hit_plan_count = self._count("main_hitweekplan")
        new_hit_entry_count = self._count("main_hitweekplanentry")

        self.stdout.write(self.style.SUCCESS("=== 3NF Fase 1 Verificatie ==="))
        self.stdout.write(f"Legacy Injury records: {old_injury_count}")
        self.stdout.write(f"Nieuwe InjuryCase records: {new_injury_count}")
        self.stdout.write(f"Legacy HitWeekPlanning records: {old_hit_count}")
        self.stdout.write(f"Nieuwe HitWeekPlan records: {new_hit_plan_count}")
        self.stdout.write(f"Nieuwe HitWeekPlanEntry records: {new_hit_entry_count}")
