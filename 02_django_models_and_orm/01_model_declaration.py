"""
MODEL DECLARATION AND DATABASE BOOTSTRAPPING
=============================================
This script demonstrates how to configure and define Django models within a
single script, utilizing an in-memory SQLite database.
"""

import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

# 1. Configure settings and initialize Django setup
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        INSTALLED_APPS=["__main__"], # Register this script module as the active app
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:", # In-memory database; vanishes after run
            }
        },
    )
    django.setup()

# 2. Define Django Model
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "__main__" # Explicitly hook this model to the '__main__' app

    def __str__(self):
        return f"{self.name} ({self.email})"

# 3. Execution code
if __name__ == "__main__":
    # Create the tables in the in-memory database on the fly
    print("[ORM] Running database schema creation...")
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # Create database records
    student1 = Student.objects.create(name="Alice", email="alice@edu.org", age=21)
    student2 = Student.objects.create(name="Bob", email="bob@edu.org", age=22)
    
    print(f"[ORM] Created student 1: {student1}")
    print(f"[ORM] Created student 2: {student2}")
    
    # Query database records count
    count = Student.objects.count()
    print(f"[ORM] Total students enrolled: {count}")
