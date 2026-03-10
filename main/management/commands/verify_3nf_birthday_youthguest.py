from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Controleert 3NF-v2 voor Birthday/YouthGuest."

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
        self.stdout.write(self.style.SUCCESS("=== Birthday/YouthGuest 3NF Verificatie ==="))
        self.stdout.write(f"Legacy Birthday: {self._count('main_birthday')}")
        self.stdout.write(f"V2 BirthdayProfile: {self._count('main_birthdayprofile')}")
        self.stdout.write(f"V2 BirthdayRecord: {self._count('main_birthdayrecord')}")
        self.stdout.write(f"Legacy YouthGuest: {self._count('main_youthguest')}")
        self.stdout.write(f"V2 YouthGuestProfile: {self._count('main_youthguestprofile')}")
        self.stdout.write(f"V2 YouthGuestWeek: {self._count('main_youthguestweek')}")
