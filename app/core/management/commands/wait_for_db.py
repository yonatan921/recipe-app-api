"""
Django command to wait for the DB to be available with a timeout.
"""

import time
import sys
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
    Django command to wait for the database with a 20-second timeout.
    """

    def handle(self, *args, **options):
        """
        Checks if the database is available. If not, waits up to 20 seconds before timing out and returning a non-zero exit code.
        """
        self.stdout.write("Waiting for database...")

        db_up = False
        start_time = time.time()  # Track the start time
        timeout = 20  # Set timeout to 20 seconds

        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    self.stderr.write(self.style.ERROR("Database not available after 20 seconds, exiting."))
                    sys.exit(1)  # Exit with a non-zero status
                self.stdout.write(self.style.ERROR("Database unavailable, retrying..."))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available"))
