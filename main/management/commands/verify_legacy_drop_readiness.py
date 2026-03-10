from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Checkt of legacy tabellen veilig richting drop kunnen."

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
        checks = [
            ("main_injury", "main_injurycase"),
            ("main_hitweekplanning", "main_hitweekplan"),
            ("main_dayprogram", "main_dayprogramentry"),
            ("main_dailyprogram", "main_individualdayplan"),
            ("main_aanwezigheid", "main_attendancerecord"),
            ("main_antropometry", "main_anthropometrysession"),
            ("main_playerintake", "main_nutritionintakesession"),
            ("main_birthday", "main_birthdayrecord"),
            ("main_youthguest", "main_youthguestweek"),
            ("main_overig", "main_overignote"),
            ("main_trainingdata", "main_performancesession"),
            ("main_wedstrijddata", "main_performancesession"),
            ("main_playertest", "main_performancesession"),
        ]

        self.stdout.write(self.style.SUCCESS("=== Legacy Drop Readiness ==="))
        ready = True

        for old_name, new_name in checks:
            old_count = self._count(old_name)
            new_count = self._count(new_name)
            line = f"{old_name}: {old_count} -> {new_name}: {new_count}"
            if old_count > 0 and new_count == 0:
                ready = False
                self.stdout.write(self.style.ERROR(f"[FAIL] {line}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"[OK] {line}"))

        entry_tables = [
            "main_hitweekplanentry",
            "main_anthropometrymeasurement",
            "main_nutritionintakeitem",
        ]

        self.stdout.write("")
        for table_name in entry_tables:
            count = self._count(table_name)
            if count == 0:
                ready = False
                self.stdout.write(self.style.WARNING(f"[WARN] {table_name}: {count}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"[OK] {table_name}: {count}"))

        self.stdout.write("")
        if ready:
            self.stdout.write(self.style.SUCCESS("READY: legacy drop kan voorbereid worden (nog niet uitvoeren zonder backup)."))
        else:
            self.stdout.write(self.style.WARNING("NOT READY: eerst ontbrekende data/sync oplossen."))
