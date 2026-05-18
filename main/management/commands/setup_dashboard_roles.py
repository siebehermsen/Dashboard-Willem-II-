from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from main.permissions import ROLE_CHOICES


class Command(BaseCommand):
    help = "Maakt de standaard dashboardrollen aan als Django Groups."

    def handle(self, *args, **options):
        created_count = 0
        for group_name, label in ROLE_CHOICES:
            _group, created = Group.objects.get_or_create(name=group_name)
            created_count += int(created)
            status = "aangemaakt" if created else "bestond al"
            self.stdout.write(f"{label}: {group_name} ({status})")

        self.stdout.write(self.style.SUCCESS(f"Dashboardrollen klaar. Nieuw aangemaakt: {created_count}."))
