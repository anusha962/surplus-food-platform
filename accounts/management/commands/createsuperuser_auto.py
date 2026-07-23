import os
from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Creates a superuser from env vars if one doesn't already exist."

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write("Skipping superuser creation - env vars not set.")
            return

        if CustomUser.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' already exists, skipping.")
            return

        CustomUser.objects.create_superuser(
            username=username, email=email or '', password=password, role=CustomUser.Role.ADMIN
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))