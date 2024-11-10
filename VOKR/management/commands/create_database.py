from django.core.management.base import BaseCommand
from django.conf import settings
import MySQLdb

class Command(BaseCommand):
    help = "Automatically create the database if it doesn't exist"

    def handle(self, *args, **kwargs):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        try:
            # Connect to MySQL server
            conn = MySQLdb.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                port=int(db_port)
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Execute SQL statement to create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            self.stdout.write(self.style.SUCCESS(f"Successfully ensured database '{db_name}' exists."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating database: {str(e)}"))
        finally:
            if conn:
                conn.close()
