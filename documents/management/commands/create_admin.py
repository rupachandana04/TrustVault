import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create an admin user from environment variables"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("BOOTSTRAP_ADMIN_USERNAME")
        email = os.environ.get("BOOTSTRAP_ADMIN_EMAIL")
        password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write("Admin environment variables not configured.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("Admin user already exists.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("Admin user created successfully."))