"""
Django command to wait for the database to start before initializing the app container
"""

import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """entrypoint for the command"""
        self.stdout.write("Waiting for database to get ready.....")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database not yet ready! Waiting 1sec...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database ready!"))
