from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Controleert backfill/sync voor DailyProgram en Aanwezigheid 3NF-v2."

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
        legacy_daily = self._count("main_dailyprogram")
        legacy_presence = self._count("main_aanwezigheid")
        new_plan = self._count("main_individualdayplan")
        new_note = self._count("main_individualdayplannote")
        new_status = self._count("main_attendancestatus")
        new_presence = self._count("main_attendancerecord")

        self.stdout.write(self.style.SUCCESS("=== DailyProgram/Aanwezigheid 3NF Verificatie ==="))
        self.stdout.write(f"Legacy DailyProgram records: {legacy_daily}")
        self.stdout.write(f"Nieuwe IndividualDayPlan records: {new_plan}")
        self.stdout.write(f"Nieuwe IndividualDayPlanNote records: {new_note}")
        self.stdout.write("")
        self.stdout.write(f"Legacy Aanwezigheid records: {legacy_presence}")
        self.stdout.write(f"Nieuwe AttendanceStatus records: {new_status}")
        self.stdout.write(f"Nieuwe AttendanceRecord records: {new_presence}")

        if legacy_daily > 0 and new_plan == 0:
            self.stdout.write(self.style.WARNING("Let op: DailyProgram lijkt nog niet gebackfilled."))
        else:
            self.stdout.write(self.style.SUCCESS("DailyProgram backfill lijkt in orde."))

        if legacy_presence > 0 and new_presence == 0:
            self.stdout.write(self.style.WARNING("Let op: Aanwezigheid lijkt nog niet gebackfilled."))
        else:
            self.stdout.write(self.style.SUCCESS("Aanwezigheid backfill lijkt in orde."))
